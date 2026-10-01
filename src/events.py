from dataclasses import dataclass


class Event:
    """Base class so every event shares a common type."""
    pass


@dataclass
class MarketEvent(Event):
    """A new bar has been revealed. Carries no data."""
    pass


@dataclass
class SignalEvent(Event):
    """The strategy's opinion: buy or sell this ticker."""
    ticker: str
    timestamp: object
    direction: str  # "BUY" or "SELL"


@dataclass
class OrderEvent(Event):
    """The portfolio manager's instruction: trade this many shares."""
    ticker: str
    timestamp: object
    direction: str  # "BUY" or "SELL"
    quantity: int
    order_type: str = "MARKET"


@dataclass
class FillEvent(Event):
    """What actually happened when the order hit the simulated market."""
    ticker: str
    timestamp: object
    direction: str
    quantity: int
    reference_price: float  # next open, before slippage
    fill_price: float       # after slippage
    commission: float