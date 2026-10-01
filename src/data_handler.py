import pandas as pd
class DataHandler:

   def __init__(self, tickers=None, folder='../data'):
      # instance attributes
      self.tickers = tickers 
      self.folder = folder
      self.still_running = True
      self.counter = 0
      self.data={}
      for ticker in self.tickers:
        path = self.folder + "/" + ticker + ".csv"
        df = pd.read_csv(path, index_col=0, parse_dates=True,skiprows=[1, 2])
        self.data[ticker] = df
      self.length = min(len(df) for df in self.data.values())
      
        

   def advance(self):
      self.counter += 1
      if self.counter > self.length:
            self.still_running = False
            return None
      return {t: self.data[t].iloc[self.counter - 1] for t in self.tickers}
   
   def get_latest_bars(self, ticker, n):
    start = max(0, self.counter - n)
    return self.data[ticker].iloc[start:self.counter]

handler = DataHandler(["AAPL"], "/Users/dakshaswam/backtesting engine/Event-driven-backtesting-engine-/data")

while handler.still_running:
   
    bar = handler.advance()          # reveal the next day
    if bar is None:                  # no data left
        break

    recent = handler.get_latest_bars("AAPL", 3)   # the last 3 revealed days

    print(handler.counter, bar["AAPL"]["Close"], len(recent))
    print(recent)
    if handler.counter == 5:         # stop early so you don't print thousands of lines
        break




    
