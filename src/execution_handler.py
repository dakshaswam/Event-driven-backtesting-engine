from events import *
from data_handler import DataHandler


class ExecutionHandler:
    def __init__(self, handler: DataHandler, queue):
        self.queue = queue
        self.handler = handler

    def execute_order(self, order: OrderEvent):
        ticker = order.ticker
        direction = order.direction
        quantity = order.quantity
        timestamp = order.timestamp

        latest_bar = self.handler.get_latest_bars(ticker, 1)
        price = latest_bar["Close"].iloc[-1]   

        fill = FillEvent(ticker, timestamp, direction, quantity, price, price, 0)
        self.queue.append(fill)