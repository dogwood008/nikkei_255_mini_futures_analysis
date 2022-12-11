from typing import Union, NewType
from datetime import datetime, timedelta
from joblib import Parallel, delayed

import pandas as pd
from pandas import DatetimeIndex

from nikkei_225_mini import Nikkei225Mini
from plotly_candle_stick import PlotlyCandleStick
from separated import Separated

import sys

class TickData:
    DatetimeLike = NewType('DatetimeLike', Union[datetime, DatetimeIndex])
    if sys.version_info.minor >= 10:
        Datetimes = NewType('DateTimes', list[DatetimeLike])
        DatetimeSet = NewType('DateTimeSet', list[tuple[datetime, datetime]])
    else:
        from typing import List, Tuple
        Datetimes = NewType('DateTimes', List[DatetimeLike])
        DatetimeSet = NewType('DateTimeSet', List[Tuple[datetime, datetime]])

    def __init__(self, from_dt: datetime, until_dt: datetime, df: Nikkei225Mini, output_base_dir: str,
                 freq: str = 'H', parallel: bool = False):
        self.from_dt = from_dt
        self.until_dt = until_dt
        self.df: Nikkei225Mini = df
        self.output_base_dir = output_base_dir
        self.parallel = parallel
        self.freq = freq
        self.graph_method: PlotlyCandleStick = Separated

    def _timedelta(self) -> dict:
        if self.freq == 'H':
            return {'hours': 1}
        elif self.freq == 'D':
            return {'days': 1}
        else:
            raise ValueError(f'freq={self.freq} is not supported')

    def _from_to_dts(self) -> Datetimes:
        return [
            [from_dt, from_dt + timedelta(**self._timedelta())]
            for from_dt in
            pd.date_range(start=self.from_dt,
                          end=self.until_dt, freq=self.freq)
        ]

    def _loop_export_procedure(self, dt_set: DatetimeSet):
        from_dt, until_dt = dt_set
        filename: str = str(from_dt)
        data: Nikkei225Mini = Nikkei225Mini(self.df.sort_index().loc[from_dt:until_dt, :])
        if len(data) == 0:
            print(f'SKIPPED: {filename}')
            return
        print(f'STARTED  : {filename}')
        self.graph_method.graph_method(
            data.convert_into_ohlcv('2S'),
            output_base_dir=self.output_base_dir,
            save_fig=True, title=from_dt, filename=from_dt
        )
        print(f'COMPLETED: {filename}')

    def export(self):
        if self.parallel:
            Parallel(n_jobs=-1)([delayed(self._loop_export_procedure)(dt)
                                 for dt in self._from_to_dts()])
        else:
            [self._loop_export_procedure(dt) for dt in self._from_to_dts()]
