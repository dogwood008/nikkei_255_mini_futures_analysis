import pandas as pd


class Nikkei225Mini(pd.DataFrame):

    @classmethod
    def read_from_csv(cls, filepath: str):
        df = cls._parse_date(
            pd.read_csv(filepath, dtype=cls._dtype())
        )
        return cls(df)

    @classmethod
    def _dtype(cls) -> dict:
        return {
            'trade_date': str,
            'make_date': str,
            'index_type': 'uint8',
            'security_code': str,
            'time': str,
            'trade_price': 'float32',
            'price_type': str,
            'trade_volume': 'uint32',
            'no': 'uint32',
            'contract_month': str,
        }

    @classmethod
    def _parse_date(cls, df) -> pd.DataFrame:
        df.trade_date = pd.to_datetime(
            df.trade_date + 'T' + df.time, format='%Y%m%dT%H%M%S%f')
        df.make_date = pd.to_datetime(
            df.make_date + 'T' + df.time, format='%Y%m%dT%H%M%S%f')
        df.index = df.make_date
        return df

    def convert_into_ohlcv(self, frequency: str) -> pd.DataFrame:
        ohlcv = self.trade_price.resample(frequency).ohlc()
        ohlcv['volume'] = self.trade_volume.resample(frequency).sum()
        return ohlcv
