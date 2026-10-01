from datetime import date
import yfinance as yf


TICKERS = ["AAPL", "TSLA", "ORCL", "MSFT"]
START_DATE = "2005-01-01"
END_DATE = date.today()
DATA_FOLDER = "data"

for ticker in TICKERS:
    print("Printing" + ticker)
    dat = yf.download(ticker, start = START_DATE, end = END_DATE)
    if(dat.empty):
        raise ValueError("No data found for this ticker.")
    dat.to_csv(f"data/{ticker}.csv")
    row_count = len(dat)
    print(f"Total rows using len(): {row_count}")

print('done')
