from collections import deque
from data_handler import DataHandler
from events import *
from stretegy import MovingAverageCrossStrategy
from portfolio import Portfolio
from execution_handler import ExecutionHandler


class Backtest:
    def __init__(self, handler: DataHandler, short_window=20, long_window=50):
        self.handler = handler
        self.queue = deque()
        self.counter = 0
        self.signals = []
        self.fills = []

        self.strategy = MovingAverageCrossStrategy(
            self.handler, self.queue, short_window, long_window
        )
        self.portfolio = Portfolio(self.handler, self.queue)
        self.execution = ExecutionHandler(self.handler, self.queue)

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
                    self.execution.fillpendingorder()
                    self.strategy.calculate_signals(event)
                    self.portfolio.record_value()

                elif isinstance(event, SignalEvent):
                    self.signals.append(event)
                    self.portfolio.signal(event)

                elif isinstance(event, OrderEvent):
                    self.execution.execute_order(event)

                elif isinstance(event, FillEvent):
                    self.fills.append(event)
                    if event.direction == "BUY":
                        self.portfolio.buy_shares(event.ticker, event.fill_price, event.quantity, event.commission)
                    elif event.direction == "SELL":
                        self.portfolio.sell_shares(event.ticker, event.fill_price, event.quantity, event.commission)