import akshare as ak
ak.__version__
hist_df = ak.stock_us_daily(symbol="AAPL")  # Get U.S. stock Amazon's price info
print(hist_df)
