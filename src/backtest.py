from collections import deque
from data_handler import DataHandler
from events import *
from stretegy import MovingAverageCrossStrategy
from portfolio import *

class Backtest:
    def __init__(self, handler: DataHandler, short_window=20, long_window=50):
        self.handler = handler
        self.queue = deque()
        self.counter = 0
        self.signals = []
        self.portfolio = Portfolio(self.handler, self.queue)
        self.strategy = MovingAverageCrossStrategy(
            self.handler, self.queue, short_window, long_window
        )

    def run(self):
        while self.handler.still_running:
            bar = self.handler.advance()
            if bar is None:
                break
            self.queue.append(MarketEvent())
            while self.queue:
                event = self.queue.popleft()

                if isinstance(event, MarketEvent):
                    self.counter += 1
                    self.strategy.calculate_signals(event)

                elif isinstance(event, SignalEvent):
                    self.portfolio.signal(event)
                    self.signals.append(event)
                    print(vars(event))

                elif isinstance(event, OrderEvent):
                    print(vars(event))

                elif isinstance(event, FillEvent):
                    pass