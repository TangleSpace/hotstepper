import sys
sys.path.insert(0, r"..")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hotstepper.basis import Bases, Basis
from hotstepper.Steps import Steps
#from hotstepper.Step import Step

import warnings
warnings.filterwarnings("ignore")


def page_view_sample():
    df = pd.read_csv(r"./data/page_views.csv")
    return Steps.read_dataframe(df,'start','ends')


def hotel_stays_sample():
    df = pd.read_csv(r"./data/hotel_stays.csv", parse_dates=['check_in', 'check_out'], dayfirst=True)
    return Steps.read_dataframe(df,'check_in','check_out',use_datetime=True)


def vessel_queue_sample():
    df = pd.read_csv(r"./data/vessel_queue.csv", parse_dates=['enter', 'leave'], dayfirst=True)
    return Steps.read_dataframe(df,'enter','leave',use_datetime=True)