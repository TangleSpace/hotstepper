import os
import pandas as pd
from hotstepper import Steps
from hotstepper import Step

import warnings
warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__),'data')

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