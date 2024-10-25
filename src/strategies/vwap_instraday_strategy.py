""" VWAP Intraday Strategy. """

import backtrader as bt

from src.indicators.vwap_intraday_indicator import VwapIntradayIndicator


class VwapIntradayStrategy(bt.Strategy):
    """
    VWAP Rolling Strategy.
    """

    def __init__(self) -> None:
        self.vwap_rolling = VwapIntradayIndicator(self.data, plot=True)  # type: ignore[attr-defined, call-arg]
