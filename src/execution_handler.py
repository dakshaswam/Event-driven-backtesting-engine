from events import *
from data_handler import DataHandler


class ExecutionHandler:
    def __init__(self, handler: DataHandler, queue):
        self.queue = queue
        self.handler = handler
        self.pendingorders = []
        self.slippage = 0.0005
        self.commission = 1

    def execute_order(self, order: OrderEvent):
        self.pendingorders.append(order)

    def fillpendingorder(self):
        for order in self.pendingorders:
            ticker = order.ticker
            direction = order.direction
            quantity = order.quantity

            latest_bar = self.handler.get_latest_bars(ticker, 1)
            reference = latest_bar["Open"].iloc[-1]
            if direction=='BUY':
                fill = reference*(1+self.slippage)
            elif direction=='SELL':
                fill = reference*(1-self.slippage)
            timestamp = latest_bar.index[-1]

            fill = FillEvent(ticker, timestamp, direction, quantity, reference, fill, self.commission)
            self.queue.append(fill)

        self.pendingorders = []