from __future__ import annotations
import numpy as np
import pandas as pd
import math
from scipy import stats
from statsmodels.tsa.tsatools import lagmat
from statsmodels.tools.tools import add_constant
from hotstepper.utilities.helpers import get_clean_step_data,prepare_input,rolling_window


def acf(steps, maxlags = 10):

    """
    Calculates the Auto Correction Function for the steps data.
    
    Parameters
    ==========
    steps : `class`::Steps
        Steps object to perform calculation.

    maxlags : int, Optional
        The maximum number of step key look backs to perform analysis.
            
    Returns
    ==========
    array, array
        
    See Also
    ==========
    Steps.histogram
    Steps.ecdf
    Steps.pacf

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Partial_autocorrelation_function

    """
    _, steps_raw = get_clean_step_data(steps)

    if (maxlags is None) or (maxlags >= len(steps_raw)):
        maxlags = len(steps_raw) - 1 

    lags = np.arange(0, maxlags+1)
    acf = np.array([np.corrcoef(steps_raw[:-lag],steps_raw[lag:])[0,1] for lag in lags[1:]])
    acf = np.insert(acf,0,1.0)

    return lags,acf

def pacf(steps, maxlags = 10):

    """
    Calculates the Partial Auto Correction Function for the steps data.
    
    Parameters
    ==========
    steps : `class`::Steps
        Steps object to perform calculation.

    maxlags : int, Optional
        The maximum number of step key look backs to perform analysis.
            
    Returns
    ==========
    array, array
        
    See Also
    ==========
    Steps.histogram
    Steps.ecdf

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Partial_autocorrelation_function

    """
    _, steps_raw = get_clean_step_data(steps)

    if (maxlags is None) or (maxlags >= len(steps_raw)):
        maxlags = len(steps_raw) - 1 

    lags = np.arange(0, maxlags+1)
    xlags, x0 = lagmat(steps_raw, maxlags, original="sep")
    xlags = add_constant(xlags)

    pacf = np.array([(np.linalg.lstsq(xlags[lag:, : lag + 1], x0[lag:], rcond=None)[0])[-1] for lag in lags[1:]])
    pacf = np.insert(pacf,0,1.0)
        
    return lags,pacf


def ecdf(steps):

    """
    Calculates the Empirical Cummulative Distribution Function for the steps data.
    
    Parameters
    ==============
    steps : `class`::Steps
        Steps object to perform calculation.
            
    Returns
    ==============
    array, array

    See Also
    ==============
    Steps.histogram    
    Steps.pacf

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Empirical_distribution_function

    """

    _, steps_raw = get_clean_step_data(steps)
    x = np.sort(steps_raw)
    y = np.arange(0, len(x),dtype=np.float) / len(x)

    return x,y


def histogram(steps, bins=None,axis=0,ts_grain = None):
    
    """
    Calculates a histogram for the corresponding step function values
    
    Parameters
    ----------
    steps : `class`::Steps
        Steps object to perform calculation.

    bins : int, Optional
        The number of bins the data will be grouped into for analysis
        
    axis : int, Optional (rows -> y values)
        The axis to use to generate the histogram.
        axis = 0; will use row data that represents the equivalent y values of the steps data.
        axis = 1; will use column data that represents the equivalent x values of the steps data.
            
    Returns
    -------
    array, array
        
    See Also
    --------
    Steps.ecdf
    Steps.pacf

    """

    interval = 0

    step_keys, steps_raw = get_clean_step_data(steps)

    if axis is None or axis == 0:
        data = steps_raw
    else:
        data = step_keys

    min_value = np.amin(data)
    max_value = np.amax(data)

    if bins is None:
        if axis != 0 and steps.using_datetime():
            interval = pd.Timedelta(minutes=1)
        else:
            interval = 1
    else:
        if axis != 0 and steps.using_datetime():
            pass
        else:
            interval = (max_value - min_value)/bins

    length = len(data)

    if axis is not None and axis > 0 and steps.using_datetime():
        rang = np.arange(min_value,max_value+interval,interval).astype(pd.Timedelta)
    else:
        rang = np.arange(min_value,max_value+interval,interval)

    return rang, [sum(np.where((data >= i) & (data < i+interval),1/length,0)) for i in rang]


def span_and_weights(st):
    step_keys, _ = get_clean_step_data(st)

    min_key = np.amin(step_keys)
    max_key = np.amax(step_keys)

    span = max_key - min_key
    span_deltas = np.diff(step_keys)
    span_deltas = np.append(span_deltas,0)
    weights = np.divide(span_deltas,span)

    return min_key,max_key,span, weights


def mean_integrate(st):
    _, steps_raw = get_clean_step_data(st)

    _,_,span, weight = span_and_weights(st)
    mean = np.dot(steps_raw,weight)
    var = np.dot(np.power(steps_raw,2),weight) - mean**2
    area = span*mean

    if st.using_datetime():
        return mean,area/3600,var
    else:
        return mean,area,var


def mean(st):
    m,_,_ = mean_integrate(st)
    return m


def var(st):
    _,_,v = mean_integrate(st)
    return v


def std(st):
    _,_,v = mean_integrate(st)
    return np.sqrt(v)


def integrate(st):
    m,a,v = mean_integrate(st)
    return a


def percentile(st, percent):
    _, steps_raw = get_clean_step_data(st)

    return np.percentile(steps_raw,percent)


def min(st, include_zero=True):
    _, steps_raw = get_clean_step_data(st)
    if not include_zero:
        steps_raw = steps_raw[steps_raw!=0]

    return np.min(steps_raw)


def max(st):
    _, steps_raw = get_clean_step_data(st)

    return np.max(steps_raw)

def median(st):
    return percentile(st,50)

def mode(st, policy='omit'):
    _, steps_raw = get_clean_step_data(st)

    m,_ = stats.mode(steps_raw,nan_policy=policy)
    return m[0]


def covariance(st,other):
    return mean(st*other) - mean(st)*mean(other)


def correlation(st,other):
    return covariance(st,other)/(std(st)*std(other))

def describe(st, precision = 2, return_dataframe = True):

    """
    Generate a table containing a number of standard statistical metrics for the steps data.
    
    """
    
    summary = {}

    _, step_values = get_clean_step_data(st)
    summary['Count'] = len(st.step_keys())

    summary['Mean'] = round(st.mean(),precision)
    summary['Median'] = round(st.median(),precision)
    summary['Mode'] = round(st.mode(),precision)
    summary['Std'] = round(st.std(),precision)
    summary['Var'] = round(st.var(),precision)
    summary['Min'] = round(st.min(),precision)
    summary['25%'] = round(st.percentile(25),precision)
    summary['75%'] = round(st.percentile(75),precision)
    summary['Max'] = round(st.max(),precision)
    summary['Area'] = round(st.integrate(),precision)

    if st.using_datetime():
        summary['Start'] = st.first()
        summary['End'] = st.last()
    else:
        summary['Start'] = round(st.first(),precision)
        summary['End'] = round(st.last(),precision)

    if return_dataframe:
        dfsummary = pd.DataFrame({'Metric': summary.keys(), 'Value':summary.values()})
        return dfsummary
    else:
        return summary

def rolling_function_step(steps,x,rolling_function=None, window = 1, pre_mid_post = 'mid'):

    """
    
    """

    if pre_mid_post == 'mid':
        start_idx = math.floor((window-1)/2)
        end_idx = -1*(math.ceil((window-1)/2))
    elif pre_mid_post == 'pre':
        start_idx = 0
        end_idx = -1*(window-1)
    else:
        start_idx = (window-1)
        end_idx = len(x)

    if (steps.step_values()).shape[0] > 0:
        x_raw = prepare_input(x)
        st = steps(x_raw)

        if rolling_function is None:
            rolling_function = np.mean
        return x[start_idx:end_idx], rolling_function(rolling_window(st,window),axis=1)
    else:
        return x, np.zeros(len(x))