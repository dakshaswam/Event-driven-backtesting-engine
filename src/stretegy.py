from events import *
from data_handler import DataHandler
class Strategy:
    def __init__(self,handler : DataHandler, queue):
        self.handler = handler 
        self.queue = queue
    def calculate_signals(self, event):
        pass

class MovingAverageCrossStrategy(Strategy):
    def __init__(self, handler, queue, short_window, long_window):
        super().__init__(handler, queue)
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, event:MarketEvent):
        if not isinstance(event, MarketEvent):
            return 

        for ticker in self.handler.tickers:
            bars = self.handler.get_latest_bars(ticker, self.long_window+1)
            if len(bars) < self.long_window + 1:
                continue

            closes = bars['Close']

            today_short = closes.iloc[-self.short_window:].mean()
            today_long = closes.iloc[-self.long_window:].mean()
            yesterday_short = closes.iloc[-self.short_window - 1:-1].mean()
            yesterday_long = closes.iloc[-self.long_window - 1:-1].mean()
            direction = None
            if yesterday_short <= yesterday_long and today_short > today_long:
                direction = "BUY"
            elif yesterday_short >= yesterday_long and today_short < today_long:
                direction = "SELL"

            signal_event = SignalEvent(ticker, bars.index[-1],direction)
            self.queue.append(signal_event)
                




