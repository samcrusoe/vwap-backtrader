""" VWAP strategy implementation """

import backtrader as bt

from src.brokers.yahoo_broker import get_ohlc_pandas_data
from src.strategies.vwap_instraday_strategy import VwapIntradayStrategy
from src.strategies.vwap_rolling_strategy import VwapRollingStrategy


if __name__ == "__main__":
    MARKET = "^GSPC"
    cerebro = bt.Cerebro()
    cerebro.addstrategy(VwapRollingStrategy)
    cerebro.addstrategy(VwapIntradayStrategy)
    data = get_ohlc_pandas_data(MARKET, "15m")
    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot(style="candlestick")
