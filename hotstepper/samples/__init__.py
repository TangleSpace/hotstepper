import os
import pandas as pd
from hotstepper import Steps
from hotstepper import Step

import warnings
warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__),'data')

# def _download_datasets_if_missing():
#     #Handy code from the Seaborn package to manage the datasets through git and a local cache.

#     path = ("https://raw.githubusercontent.com/"
#                 "mwaskom/seaborn-data/master/{}.csv")
#         full_path = path.format(name)

#         if cache:
#             cache_path = os.path.join(get_data_home(data_home),
#                                     os.path.basename(full_path))
#             if not os.path.exists(cache_path):
#                 if name not in get_dataset_names():
#                     raise ValueError(f"'{name}' is not one of the example datasets.")
#                 urlretrieve(full_path, cache_path)
#             full_path = cache_path

def page_view_sample():
    df = pd.read_csv(os.path.join(DATA_DIR,'page_views.csv'))
    return Steps.read_dataframe(df,'start','ends')


def hotel_stays_sample():
    df = pd.read_csv(os.path.join(DATA_DIR,'hotel_stays.csv'), parse_dates=['check_in', 'check_out'], dayfirst=True)
    return Steps.read_dataframe(df,'check_in','check_out',use_datetime=True)


def vessel_queue_sample():
    df = pd.read_csv(os.path.join(DATA_DIR,'vessel_queue.csv'), parse_dates=['enter', 'leave'], dayfirst=True)
    return Steps.read_dataframe(df,'enter','leave',use_datetime=True)


def daily_temperature_sample():
    df = pd.read_csv(os.path.join(DATA_DIR,'daily-min-temperatures.csv'),parse_dates=['Date'])
    return Steps.read_dataframe(df,start='Date',weight='Temp',convert_delta=True)