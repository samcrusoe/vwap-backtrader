""" Yahoo Finance broker module """

import backtrader as bt
import yfinance as yf

TIMEFRAME_MAP = {
    "1m": (bt.TimeFrame.Minutes, 1),
    "2m": (bt.TimeFrame.Minutes, 2),
    "5m": (bt.TimeFrame.Minutes, 5),
    "15m": (bt.TimeFrame.Minutes, 15),
    "30m": (bt.TimeFrame.Minutes, 30),
    "60m": (bt.TimeFrame.Minutes, 60),
    "90m": (bt.TimeFrame.Minutes, 90),
    "1h": (bt.TimeFrame.Minutes, 60),
    "1d": (bt.TimeFrame.Days, 1),
    "5d": (bt.TimeFrame.Days, 5),
    "1wk": (bt.TimeFrame.Weeks, 1),
    "1mo": (bt.TimeFrame.Months, 1),
    "3mo": (bt.TimeFrame.Months, 3),
}


def get_ohlc_pandas_data(market: str, timeframe: str) -> bt.feeds.PandasData:
    """
    Fetch OHLC data from Yahoo Finance and convert it to a Backtrader data feed.

    Parameters:
    - market (str): Trading symbol (e.g., "^GSPC" for S&P 500)
    - timeframe (str): Data timeframe (e.g., "1d", "1h", "15m")
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    Returns:
    - bt.feeds.PandasData: Backtrader data feed
    """
    data_source = yf.Ticker(market)
    df = data_source.history(interval=timeframe)
    df.index = df.index.tz_convert("UTC")
    bt_timeframe, compression = TIMEFRAME_MAP.get(timeframe, (bt.TimeFrame.Minutes, 1))
    # ignore pylint E1123:
    data = bt.feeds.PandasData(dataname=df, timeframe=bt_timeframe, compression=compression)  # pylint: disable=E1123

    return data
