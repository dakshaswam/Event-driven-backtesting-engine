import pandas as pd


def equity_series(equity_curve):
    """Turn the portfolio's list of (date, value) pairs into a Series indexed by date."""
    dates = [d for d, _ in equity_curve]
    values = [float(v) for _, v in equity_curve]
    return pd.Series(values, index=pd.DatetimeIndex(dates), name="equity")


def total_return(equity):
    return equity.iloc[-1] / equity.iloc[0] - 1


def annual_return(equity):
    days = (equity.index[-1] - equity.index[0]).days
    if days <= 0:
        return 0.0
    years = days / 365.25
    return (1 + total_return(equity)) ** (1 / years) - 1


def drawdown_series(equity):
    """How far below its previous peak the curve is on each day (0 = at a new high)."""
    return equity / equity.cummax() - 1


def max_drawdown(equity):
    return drawdown_series(equity).min()


def buy_and_hold(closes, starting_cash):
    """Value over time of putting all starting cash into the stock on day one."""
    return starting_cash * closes / closes.iloc[0]


def summary(equity):
    return {
        "final_value": equity.iloc[-1],
        "total_return": total_return(equity),
        "annual_return": annual_return(equity),
        "max_drawdown": max_drawdown(equity),
    }