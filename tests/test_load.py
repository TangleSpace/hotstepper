import os
import sys
sys.path.insert(0, r"..//")

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hotstepper import Step
from hotstepper import Steps
import hotstepper.samples as samples


def test_load_array():
    df_data = pd.read_excel('https://raw.githubusercontent.com/TangleSpace/hotstepper-data/master/data/superstore.xls',parse_dates=['Order Date','Ship Date'])
    sales_orders_df = Steps.read_dataframe(
        df_data, #the dataframe we will read from
        start='Order Date', #field name of the start keys
        end='Ship Date', #field name of the end keys
        weight='Profit') #field name of the weight or value of each step

    assert sales_orders_df.using_datetime() == True

    sales_orders_arr = Steps.read_array(
            start=df_data['Order Date'], #array of values for the start keys
            end=df_data['Ship Date'],    #array of values for the end keys
            weight=df_data['Profit'])    #array of values for the step weights or values

    assert sales_orders_arr.using_datetime() == True

    assert sales_orders_df.compare(sales_orders_arr)

