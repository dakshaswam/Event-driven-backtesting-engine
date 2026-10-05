from events import *
from data_handler import DataHandler


class Portfolio:
    def __init__(self, handler: DataHandler, shared_queue, starting_cash=100000, invest_fraction=0.99):
        self.cash = starting_cash
        self.starting_cash = starting_cash
        self.invest_fraction = invest_fraction   # share of cash to spend on a BUY
        self.shares = {}
        self.shared_queue = shared_queue
        self.handler = handler
        self.equity_curve = []

    def buy_shares(self, ticker, price, quantity, commission):
        self.cash -= price * quantity + commission
        self.shares[ticker] = self.shares.get(ticker, 0) + quantity

    def sell_shares(self, ticker, price, quantity, commission):
        self.cash += price * quantity - commission
        self.shares[ticker] = self.shares.get(ticker, 0) - quantity

    def signal(self, signalevent: SignalEvent):
        ticker = signalevent.ticker
        direction = signalevent.direction
        timestamp = signalevent.timestamp

        shares = self.shares.get(ticker, 0)

        if direction == "BUY" and shares == 0:
            price = self.handler.get_latest_bars(ticker, 1)["Close"].iloc[-1]
            budget = self.cash * self.invest_fraction
            quantity = int(budget / price)
            if quantity <= 0:
                return
            event = OrderEvent(ticker, timestamp, direction, quantity)
        elif direction == "SELL" and shares > 0:
            event = OrderEvent(ticker, timestamp, direction, shares)
        else:
            return

        self.shared_queue.append(event)

    def record_value(self):
        total = self.cash
        date = None

        for ticker in self.handler.tickers:
            latest_bar = self.handler.get_latest_bars(ticker, 1)
            price = latest_bar["Close"].iloc[-1]
            date = latest_bar.index[-1]
            total += self.shares.get(ticker, 0) * price

        self.equity_curve.append((date, total))