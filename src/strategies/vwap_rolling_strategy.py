""" VWAP Rolling Strategy """

import backtrader as bt

from src.indicators.vwap_rolling_indicator import VwapRollingIndicator


class VwapRollingStrategy(bt.Strategy):
    """
    VWAP Rolling Strategy.
    """

    params = {"period": 14}

    def __init__(self) -> None:
        self.vwap_rolling = VwapRollingIndicator(self.data, period=self.p.period, plot=True)  # type: ignore[attr-defined, call-arg]
