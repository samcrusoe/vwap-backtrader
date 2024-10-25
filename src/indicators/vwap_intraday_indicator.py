""" Volume Weighted Average Price (VWAP) indicator for intraday trading. """

import datetime
from typing import Optional

import pytz
import backtrader as bt


class VwapIntradayIndicator(bt.Indicator):
    """
    Volume Weighted Average Price (VWAP) indicator for intraday trading.
    """

    lines = ("vwap_intraday",)
    params = {"timezone": "America/New_York"}
    plotinfo = {"subplot": False}
    plotlines = {"vwap_intraday": {"color": "blue"}}

    def __init__(self) -> None:
        self.hlc = (self.data.high + self.data.low + self.data.close) / 3.0

        self.current_date: Optional[datetime.date] = None
        self.previous_date_index: int = -1

    def next(self) -> None:
        current_date = (
            pytz.utc.localize(self.data.datetime.datetime()).astimezone(pytz.timezone(self.p.timezone)).date()
        )
        len_self: int = len(self)

        if self.current_date != current_date:
            self.current_date = current_date
            self.previous_date_index = len_self - 1

        volumes = self.data.volume.get(size=len_self - self.previous_date_index)
        hlc = self.hlc.get(size=len_self - self.previous_date_index)

        numerator = sum(hlc[i] * volumes[i] for i in range(len(volumes)))
        self.lines.vwap_intraday[0] = None if sum(volumes) == 0 else numerator / sum(volumes)  # type: ignore[attr-defined]
