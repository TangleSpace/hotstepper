import os
import pandas as pd
from hotstepper import Steps
from hotstepper import Step
import urllib.parse as parse
from urllib.request import urlopen, urlretrieve

import warnings
warnings.filterwarnings("ignore")


def download_samples_if_missing(DATA_DIR):
    remote_path = ("https://raw.githubusercontent.com/tanglespace/hotstepper-data/master/{}")

    name = 'sources'
    full_path = remote_path.format(name)

    file_list = urlopen(full_path).read().decode('utf-8').split('\n')

    for file in file_list:
        if '/' in file:
            dmk, fname = file.split('/')
            folder_path = os.path.join(DATA_DIR,dmk)

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            cache_path = os.path.join(DATA_DIR,dmk,fname)
        else:
            cache_path = os.path.join(DATA_DIR,file)

        remote_file = remote_path.format('data/' + parse.quote(file))
        if not os.path.exists(cache_path):
            urlretrieve(remote_file,cache_path)


DATA_DIR = os.path.join(os.path.dirname(__file__),'data')

if not os.path.exists(DATA_DIR):
    print('Downloading HotStepper sample data, please wait.....')
    os.mkdir(DATA_DIR)
    download_samples_if_missing(DATA_DIR)
    print('HotStepper samples data download.....complete, enjoy.')
        

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