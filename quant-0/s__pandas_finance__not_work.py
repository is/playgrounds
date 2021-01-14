# not work...
# https://github.com/davidastephens/pandas-finance
# pip install pandas-finance

from pandas_finance import Equity
aapl = Equity('AAPL')
aapl.annual_dividend
aapl.dividend_yield
aapl.price
aapl.options
aapl.hist_vol(30)
aapl.rolling_hist_vol(30)
