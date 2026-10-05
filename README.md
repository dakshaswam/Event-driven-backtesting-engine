Event-Driven Backtesting Engine
An event-driven backtester written in Python that replays historical price data one bar at a time and passes events through a shared queue: market data triggers the strategy, signals become orders in the portfolio, and orders are filled by a simulated execution handler at the next bar's open with slippage and commission. It currently includes a moving average crossover strategy, all-in position sizing, an equity curve with return and drawdown metrics, and a Streamlit dashboard comparing the strategy to buy-and-hold.
pip install -r requirements.txt
streamlit run app.py
Place daily price CSVs (e.g. AAPL.csv) in a data/ folder before running.
Currently in progress: adding more strategies (RSI, breakout, buy-and-hold as a benchmark strategy) that can be swapped in from the dashboard.
