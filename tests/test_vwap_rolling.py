import unittest
import backtrader as bt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.indicators.vwap_rolling_indicator import VwapRollingIndicator


class TestVwapRollingIndicator(unittest.TestCase):
    def setUp(self):
        self.cerebro = bt.Cerebro()
        self.data = self._create_test_data()
        self.cerebro.adddata(self.data)

    def _create_test_data(self):
        dates = pd.date_range(start="2024-01-01", periods=20, freq="D")

        # Create predictable test data
        high = np.array([10.0, 11.0, 12.0, 13.0, 14.0] * 4)
        low = np.array([9.0, 10.0, 11.0, 12.0, 13.0] * 4)
        close = np.array([9.5, 10.5, 11.5, 12.5, 13.5] * 4)
        volume = np.array([100, 200, 300, 400, 500] * 4)

        df = pd.DataFrame(
            {"high": high, "low": low, "close": close, "volume": volume, "openinterest": [0] * len(dates)}, index=dates
        )

        return bt.feeds.PandasData(dataname=df)

    def test_indicator_initialization(self):
        strategy = self._create_test_strategy()
        self.cerebro.addstrategy(strategy)
        results = self.cerebro.run()

        # Check if the indicator was created
        self.assertIsNotNone(results[0].vwap)

    def _create_test_strategy(self):

        class TestStrategy(bt.Strategy):
            def __init__(self):
                self.vwap = VwapRollingIndicator()

        return TestStrategy
