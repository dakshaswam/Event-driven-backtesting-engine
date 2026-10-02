from data_handler import *
from collections import deque
from events import *
class Backtest:
    def __init__(self, handler):
        self.handler = handler
        self.queue = deque()
        self.counter = 0

    def run(self):
        while self.handler.still_running:
            bar = self.handler.advance()
            if bar is None:
                break
            self.queue.append(MarketEvent())
            while self.queue:
                event = self.queue.popleft()
                if isinstance(event, MarketEvent):
                    self.counter +=1
                elif isinstance(event, SignalEvent):
                    pass
                elif isinstance(event, OrderEvent):
                    pass
                elif isinstance(event, FillEvent):
                    pass
                




