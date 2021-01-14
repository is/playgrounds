# https://github.com/cuemacro/findatapy
# pip install findatapy
# pip install git+https://github.com/cuemacro/findatapy.git

from findatapy.market import Market, MarketDataRequest, MarketDataGenerator

market = Market(market_data_generator=MarketDataGenerator())

md_request = MarketDataRequest(
    start_date='year', category='fx',
    data_source='quandl', tickers=['EURUSD'])

df = market.fetch_market(md_request)
print(df.tail(n=10))

