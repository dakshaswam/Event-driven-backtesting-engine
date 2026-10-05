import os
import sys

import altair as alt
import pandas as pd
import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
DATA_DIR = os.path.join(ROOT, "data")

from data_handler import DataHandler
from backtest import Backtest
import metrics


st.set_page_config(page_title="Backtester", layout="wide")
st.title("Moving Average Crossover Backtest")


@st.cache_data(show_spinner="Running backtest...")
def run_backtest(ticker, short_window, long_window):
    handler = DataHandler([ticker], DATA_DIR)
    bt = Backtest(handler, short_window=short_window, long_window=long_window)
    bt.run()

    equity = metrics.equity_series(bt.portfolio.equity_curve)
    closes = handler.data[ticker]["Close"].loc[equity.index]
    fills = pd.DataFrame([vars(f) for f in bt.fills])
    return equity, closes, fills, bt.portfolio.starting_cash


# ---------- Sidebar ----------
tickers = sorted(f[:-4] for f in os.listdir(DATA_DIR) if f.endswith(".csv"))
if not tickers:
    st.error(f"No CSV files found in {DATA_DIR}")
    st.stop()

with st.sidebar:
    st.header("Settings")
    default = tickers.index("AAPL") if "AAPL" in tickers else 0
    ticker = st.selectbox("Ticker", tickers, index=default)
    short_window = st.slider("Short window (days)", 5, 100, 20)
    long_window = st.slider("Long window (days)", 20, 300, 50)
    log_scale = st.checkbox("Log scale on equity chart", value=True)

if short_window >= long_window:
    st.warning("The short window must be smaller than the long window.")
    st.stop()


# ---------- Run ----------
equity, closes, fills, starting_cash = run_backtest(ticker, short_window, long_window)
bh = metrics.buy_and_hold(closes, starting_cash)

strat = metrics.summary(equity)
bench = metrics.summary(bh)


# ---------- Metric cards ----------
def money(x):
    return f"${x:,.0f}"


def pct(x):
    return f"{x:+.1%}"


st.subheader("Strategy")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Final value", money(strat["final_value"]))
c2.metric("Total return", pct(strat["total_return"]))
c3.metric("Annual return", pct(strat["annual_return"]),
          delta=f"{strat['annual_return'] - bench['annual_return']:+.1%} vs B&H")
c4.metric("Max drawdown", pct(strat["max_drawdown"]),
          delta=f"{strat['max_drawdown'] - bench['max_drawdown']:+.1%} vs B&H")
c5.metric("Trades", len(fills))

st.subheader("Buy & hold")
b1, b2, b3, b4, _ = st.columns(5)
b1.metric("Final value", money(bench["final_value"]))
b2.metric("Total return", pct(bench["total_return"]))
b3.metric("Annual return", pct(bench["annual_return"]))
b4.metric("Max drawdown", pct(bench["max_drawdown"]))


# ---------- Equity chart ----------
st.subheader("Equity curve")
equity_df = (
    pd.DataFrame({"Strategy": equity, "Buy & hold": bh})
    .rename_axis("Date")
    .reset_index()
    .melt("Date", var_name="Series", value_name="Value")
)
equity_chart = (
    alt.Chart(equity_df)
    .mark_line()
    .encode(
        x="Date:T",
        y=alt.Y("Value:Q", title="Portfolio value ($)",
                scale=alt.Scale(type="log" if log_scale else "linear")),
        color="Series:N",
        tooltip=["Date:T", "Series:N", alt.Tooltip("Value:Q", format="$,.0f")],
    )
    .interactive()
)
st.altair_chart(equity_chart, width="stretch")


# ---------- Drawdown chart ----------
st.subheader("Drawdown")
dd_df = (
    pd.DataFrame({
        "Strategy": metrics.drawdown_series(equity),
        "Buy & hold": metrics.drawdown_series(bh),
    })
    .rename_axis("Date")
    .reset_index()
    .melt("Date", var_name="Series", value_name="Drawdown")
)
dd_chart = (
    alt.Chart(dd_df)
    .mark_line()
    .encode(
        x="Date:T",
        y=alt.Y("Drawdown:Q", axis=alt.Axis(format="%")),
        color="Series:N",
        tooltip=["Date:T", "Series:N", alt.Tooltip("Drawdown:Q", format=".1%")],
    )
    .interactive()
)
st.altair_chart(dd_chart, width="stretch")


# ---------- Trades ----------
st.subheader("Trades")
if fills.empty:
    st.write("No trades for these settings.")
else:
    table = fills[["timestamp", "direction", "quantity", "fill_price", "commission"]].copy()
    table["timestamp"] = pd.to_datetime(table["timestamp"]).dt.date
    table["fill_price"] = table["fill_price"].astype(float).round(2)
    st.dataframe(table, width="stretch", hide_index=True)