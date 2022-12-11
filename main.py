# get_ipython().run_line_magic('pip', 'install mplfinance plotly joblib')
# get_ipython().run_line_magic('pip', 'install -U kaleido')

# %pip install mplfinance
import time
from datetime import datetime
# import seaborn as sns

from tick_data import TickData
from nikkei_225_mini import Nikkei225Mini

# %matplotlib inline

# %pip install plotly
# %pip install -U kaleido

# tips = sns.load_dataset('tips')

# https://note.nkmk.me/python-joblib-parallel-usage/
# %pip install joblib


def main(df):
    td = TickData(
        from_dt=datetime(2022, 8, 1, 8, 30, 0),
        until_dt=datetime(2022, 8, 1, 10, 30, 0),
        df=df,
        output_base_dir='./figures'
    )
    td.export()


DEBUG = True
filepath = './data/日経225mini　歩み値（ティック） (2022 08).zip'
print(f'Load from zip (csv): {filepath}')

t = time.time()
df = Nikkei225Mini.read_from_csv(filepath)
print(f'Load Elapsed: {(time.time() - t):.3f}s')

main(df)
