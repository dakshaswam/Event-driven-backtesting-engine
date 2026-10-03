from events import *
from data_handler import *
class Portfolio:
    def __init__(self, handler : DataHandler, shared_queue):
        self.cash = 100000
        self.shares = {}
        self.shared_queue = shared_queue
        self.handler = handler 
        self.quantity = 100
        self.equitycurve = []

    def buy_shares(self, ticker, price):
        self.cash = self.cash - (price * self.quantity)
        if ticker in self.shares:
            self.shares[ticker] += self.quantity
        else:
            self.shares[ticker] = self.quantity

    def sell_shares(self, ticker, price):
            self.cash = self.cash + (price * self.quantity)
            if ticker in self.shares:
                self.shares[ticker] -= self.quantity
            else:
                pass

    def signal(self, signalevent: SignalEvent):
        ticker = signalevent.ticker
        direction = signalevent.direction
        timestampa = signalevent.timestamp

        shares = self.shares.get(ticker, 0)

        if direction == "BUY" and shares == 0:
            event = OrderEvent(ticker,timestampa ,direction, self.quantity)
        elif direction == "SELL" and shares > 0:
            event = OrderEvent(ticker,timestampa ,direction, shares)    

        else:
            return 

        self.shared_queue.append(event)

    def recordvalue(self):
        total = self.cash
        date = None

        for tickers in self.handler.tickers:
            latest = self.handler.get_latest_bars(tickers,1)
            price = latest['Close'].iloc[-1]
            date = latest.index[-1]

            shares_held = self.shares.get(tickers, 0)
            total += shares_held * price

        self.equitycurve.append((date, total))


