# https://github.com/ranaroussi/yfinance
# pip install yfinance --upgrade --no-cache-dir

import yfinance as yf

data = yf.download(tickers='AAPL',
    period='5d', interval='1m', auto_adjust = True)
print(data)
