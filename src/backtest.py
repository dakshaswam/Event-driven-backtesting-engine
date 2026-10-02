from collections import deque
from data_handler import DataHandler
from events import *
from stretegy import MovingAverageCrossStrategy   # change to "strategy" if you renamed the file


class Backtest:
    def __init__(self, handler: DataHandler, short_window=20, long_window=50):
        self.handler = handler
        self.queue = deque()
        self.counter = 0
        self.signals = []

        # Created once, sharing this backtest's handler and queue
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
                    # No portfolio yet, so just record and show the signal
                    self.signals.append(event)
                    print(vars(event))

                elif isinstance(event, OrderEvent):
                    pass

                elif isinstance(event, FillEvent):
                    pass