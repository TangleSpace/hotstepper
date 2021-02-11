from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import pytz
from datetime import datetime, timedelta


#########################################################################
#-----------------------methods taken from staircaes---------------------
#########################################################################
# def _set_default_timezone(tz=None):
#     global tz_default
#     tz_default = pytz.timezone(tz) if tz else None
    
# def _get_default_timezone():
#     return tz_default
    
# def _get_default_use_dates():
#     return use_dates_default
    
# def _verify_window(left_delta, right_delta, zero):
#     assert left_delta <= zero, "left_delta must not be positive"
#     assert right_delta >= zero, "right_delta must not be negative"
#     assert right_delta - left_delta > zero, "window length must be non-zero"
    
# def _check_binop_timezones(first, second):
#     assert first.tz == second.tz, "operands must have the same timezone, or none at all"

# def _convert_date_to_float(val, tz=None):
#     if val is None:
#         return None
#     if hasattr(val, "__iter__"):
#         if not isinstance(val, pd.Series):
#             val = pd.Series(val)
#         #if val.dt.tz is None and tz is not None:
#         #    val = val.dt.tz_localize(tz)
#         deltas = pd.TimedeltaIndex(val - origin.tz_localize(tz))
#         return list(deltas/pd.Timedelta(1, 'h'))
#     #if val.tz is None and tz is not None:
#     #    val = val.tz_localize(tz)
#     return (val - origin.tz_localize(tz))/pd.Timedelta(1, 'h')
    
# def _convert_float_to_date(val, tz=None):
#     if hasattr(val, "__iter__"):
#         if not isinstance(val, np.ndarray):
#             val = np.array(val)
#         return list(pd.to_timedelta(val*3600, unit='s') + origin.tz_localize(tz))
#     return pd.to_timedelta(val*3600, unit='s') + origin.tz_localize(tz)
#########################################################################
#-----------------------methods taken from staircaes---------------------
#########################################################################

#all the valid value types we can process without error
valid_input_types = (int,float,pd.Timestamp,datetime,np.datetime64,np.int,np.float,np.float64,np.int32)

def get_clean_step_data(st):
    steps_raw = st.step_values()
    step_keys = st.step_keys()

    if step_keys[0] == -np.inf:
        steps_raw = steps_raw[1:]
        step_keys = step_keys[1:]

    if step_keys[-1] == np.inf:
        steps_raw = steps_raw[:-1]
        step_keys = step_keys[:-1]

    return step_keys, steps_raw

def is_date_time(value):
    return (hasattr(value,'timestamp') and callable(value.timestamp)) or isinstance(value,np.datetime64)

def is_delta_datetime(value):
    return isinstance(value,timedelta) and isinstance(value,pd.Timedelta) or isinstance(value,np.timedelta64)

def date_to_float(date_value):
    if is_date_time(date_value):
        if isinstance(date_value,np.datetime64):
            return float(date_value)/10.0**9
        else:
            # convert all times to utc
            return (pytz.utc.localize(date_value.tz_localize(None))).timestamp()
    elif is_delta_datetime(date_value):
        return timedelta_to_float(date_value)
    else:
        raise TypeError('Only datetime, numpy.datetime64, Pandas.Timestamp and derived datetime types are valid.')


def float_to_date(float_value):
    if float_value <= get_epoch_start(False):
        return get_epoch_start(True)
    elif float_value >= get_epoch_end(False):
        return get_epoch_end(True)
    else:
        return pd.Timestamp(float_value*10.0**9)


def input_types():
    return valid_input_types


def get_default_plot_color():
    return '#9c00ff'


def get_default_plot_size():
    return (16,8)


def get_epoch_start(use_datetime = True):
    if use_datetime:
        return pd.Timestamp(1999,12,31,23,59)
    else:
        return -np.inf


def get_epoch_end(use_datetime = True):
    if use_datetime:
        return pd.Timestamp.max
    else:
        return np.inf


def timedelta_to_float(dt_delta):
    if is_delta_datetime(dt_delta):
        if isinstance(dt_delta,pd.Timedelta):
            return float(dt_delta.value/10**9)
        elif isinstance(dt_delta,datetime.timedelta):
            return float(dt_delta.seconds)
        elif isinstance(dt_delta,np.timedelta64):
            return dt_delta/np.timedelta64(1,'s')
    else:
        raise TypeError('Only datetime.timedelta, numpy.timedelta64, Pandas.Timedelta and derived datetime interval types are valid.')


def get_value(val, is_dt = False):
    if is_dt:
        return date_to_float(val)
    else:
        return val


def simple_plot(xdata,ydata,cdata=None, ax=None,**kargs):
    """
    A quick and easy way to plot 2 or 3 dimensional data in any type of plot provided by Pandas plot.

    """

    if ax is None:
        plot_size = kargs.pop('figsize',None)
        if plot_size is None:
            plot_size = get_default_plot_size()
            
        _, ax = plt.subplots(figsize=plot_size)

    dfplot = pd.DataFrame()
    dfplot['x'] = xdata
    dfplot['y'] = ydata

    if kargs.get('color') is None:
        kargs['color']=get_default_plot_color()

    if cdata is None:
        dfplot.plot(x='x',y='y', ax=ax, **kargs)
    else:
        dfplot['c'] = cdata
        dfplot.plot(x='x',y='y', c='c', ax=ax, **kargs)

    return ax


def _prettyplot(step_dict,plot_start=0,plot_start_value=0,ax=None,start_index=1,end_index=None,include_end=True,**kargs):

    step0_k = plot_start
    step0_v = plot_start_value

    if ax is None:
        plot_size = kargs.pop('figsize',None)
        if plot_size is None:
            plot_size = get_default_plot_size()
            
        _, ax = plt.subplots(figsize=plot_size)

    if kargs.get('color') is None:
        kargs['color']=get_default_plot_color()

    if end_index is None:
        end_index = len(step_dict)-1

    if start_index == 0:
        start_index = 1
    
    for i, (k,v) in enumerate(step_dict.items()):
        ax.hlines(y = step0_v, xmin = step0_k, xmax = k,**kargs)
        ax.vlines(x = k, ymin = step0_v, ymax = v,linestyles=':',**kargs)

        if i > start_index - 1 and i < end_index:
            if i == start_index:
                ax.plot(k,v,marker='o',fillstyle='none',**kargs)
            else:
                ax.plot(k,step0_v,marker='o',fillstyle='none',**kargs)
                ax.plot(k,v,marker='o',fillstyle='none',**kargs)
        elif i == end_index and include_end:
            ax.plot(k,step0_v,marker='o',fillstyle='none',**kargs)

        step0_k = k
        step0_v = v


def get_plot_range(start,end, delta = None, use_datetime = False):
    """
    
    """

    shift = None
    use_datetime = is_date_time(start) or use_datetime
    if use_datetime:
        start = pd.to_datetime(start)
        if end is not None:
            end = pd.to_datetime(end)
            shift = end - start
            span_seconds = shift.value

            if delta is None:
                if int(0.01*span_seconds) > 0:
                    delta = pd.Timedelta(nanoseconds=int(0.005*span_seconds))
                else:
                    delta = pd.Timedelta(seconds=10)
            return np.arange(start-shift, end + shift, delta).astype(pd.Timestamp)
        else:
            if start.hour > 0:
                shift = pd.Timedelta(hours=5)
                delta = pd.Timedelta(hours=1)
            elif start.minute > 0:
                shift = pd.Timedelta(minutes=6)
                delta = pd.Timedelta(minutes=2)
            else:
                shift = pd.Timedelta(hours=36)
                delta = pd.Timedelta(hours=12)
            return np.arange(start-shift, start + shift, delta).astype(pd.Timestamp)
    else:
        if end is not None:
            shift = 0.5*(end - start)

            if delta is None:
                delta = 0.1*shift

            return np.arange(start-shift, end + shift, delta)
        else:
            shift = 0.1*start

            if delta is None:
                delta = 0.1*shift

            return np.arange(start-shift, start + shift, delta)

def rolling_window(arr, window):
    shape = arr.shape[:-1]+(arr.shape[-1]-window+1, window)
    strides = arr.strides + (arr.strides[-1],)
    return np.lib.stride_tricks.as_strided(arr,shape=shape,strides=strides)
    

def get_ts(ts):
    return date_to_float(ts)


def ts_to_dt(val, is_dt=False):
    if is_dt:
        return get_dt(val)
    else:
        return val


def get_dt(ts):
    if is_date_time(ts):
        return ts
    else:
        if pd.isnull(ts) or ts <= -np.inf:
            return get_epoch_start(True)
        else:
            return float_to_date(ts)


def process_slice(sl):
    """
    """

    x = sl
    if type(sl) is slice:
        if is_date_time(sl.start):
            if sl.step is None:
                x = np.arange(sl.start,sl.stop,pd.Timedelta(minutes=1)).astype(pd.Timestamp)
            else:
                x = np.arange(sl.start,sl.stop,sl.step).astype(pd.Timestamp)
        else:
            if sl.step is None:
                x = np.arange(sl.start,sl.stop,0.001)
            else:
                x = np.arange(sl.start,sl.stop,sl.step)
    elif not hasattr(sl,'__iter__'):
        x = [sl]

    return x

def prepare_datetime(x, return_dt=True):
    """

    """

    x = process_slice(x)
    
    #either we expanded using the slice or wrapped the input in an iter
    #NOTE: Always return sorted for performance
    if is_date_time(x[0]) and return_dt:
        return np.sort(x)
    else:
        return np.sort(np.asarray(list(map(get_dt, x))).astype(pd.Timestamp))


def prepare_input(x):
    """
    
    """

    x = process_slice(x)

    #either we expanded using the slice or wrapped the input in an iter
    #NOTE: Always return sorted for performance
    if is_date_time(x[0]):
        return np.sort(np.asfarray(list(map(get_ts, x))))
    else:
        return np.sort(np.asfarray(x))


def steps_plot(steps,method=None,smooth_factor = None,smooth_basis=None,ts_grain = None,ax=None,where='post',**kargs):
    """
    
    """

    if ax is None:
        plot_size = kargs.pop('figsize',None)
        if plot_size is None:
            plot_size = get_default_plot_size()
            
        _, ax = plt.subplots(figsize=plot_size)

    if kargs.get('color') is None:
        kargs['color']=get_default_plot_color()

    if method == 'pretty':
        if steps.step_values().shape[0] == 0:
            ax.axhline(steps(0)[0], **kargs)
        else:
            _prettyplot(steps.step_values(),plot_start=steps.first(),plot_start_value=0,ax=ax,**kargs)

    elif method == 'function':
            tsx = get_plot_range(steps.first(),steps.last(),ts_grain,use_datetime=steps.using_datetime())
            ax.step(tsx,steps.step(tsx), where=where, **kargs)
            
    elif method == 'smooth':
        np_keys = steps.step_keys()
        
        # small offset to ensure we plot the initial step transition
        if steps.using_datetime():
            ts_grain = pd.Timedelta(minutes=1)
            np_keys = prepare_datetime(np_keys)
        else:
            ts_grain = 0.0000001
            
        if np_keys[0] == get_epoch_start(steps.using_datetime()):
            np_keys[0] = np_keys[1] - ts_grain
        else:
            np_keys[0] = np_keys[0] - ts_grain

        ax.plot(np_keys,steps.smooth_step(np_keys,smooth_factor = smooth_factor, smooth_basis=smooth_basis), **kargs)

    else:
        np_keys = steps.step_keys()
        np_values = steps.step_values()
        # small offset to ensure we plot the initial step transition
        if steps.using_datetime():
            ts_grain = pd.Timedelta(minutes=1)
            np_keys = prepare_datetime(np_keys)
        else:
            ts_grain = 0.0000001
        
        if np_keys[0] == get_epoch_start(steps.using_datetime()):
            np_keys[0] = np_keys[1] - ts_grain
        else:
            np_keys = np.insert(np_keys,0,np_keys[0] - ts_grain)
            np_values = np.insert(np_values,0,0)
            np_keys[0] = np_keys[0] - ts_grain

        if len(np_keys) == 0: # or ((np.abs(np_keys) == np.inf).all()):
            ax.axhline(steps(get_epoch_start(steps.using_datetime()))[0], **kargs)
        else:
            ax.step(np_keys,np_values, where=where, **kargs)

    return ax


def step_plot(step,method=None,smooth_factor = None, ts_grain = None,ax=None,where='post',**kargs):
    """
    
    """

    if ax is None:
        plot_size = kargs.pop('figsize',None)
        if plot_size is None:
            plot_size = get_default_plot_size()
            
        _, ax = plt.subplots(figsize=plot_size)

    if kargs.get('color') is None:
        kargs['color']=get_default_plot_color()

    if step.end() is None:
        max_ts = float(1.2*step._start_ts)
    else:
        max_ts = float(1.2*step._end.start_ts())

    if step._start == get_epoch_start(step.using_datetime()):
        min_ts = float(0.8*max_ts)
    else:
        min_ts = float(0.8*step._start_ts)

    if step.using_datetime():
        if ts_grain==None:
            ts_grain = pd.Timedelta(minutes=10)
            
        min_value = pd.Timestamp.utcfromtimestamp(min_ts)
        max_value = pd.Timestamp.utcfromtimestamp(max_ts)

    else:
        if ts_grain==None:
            ts_grain = 0.01
        
        min_value = min_ts-ts_grain
        max_value = max_ts+ts_grain

    end_start = step._end._start if step._end is not None else None
    tsx = get_plot_range(step._start,end_start,ts_grain,use_datetime=step.using_datetime())

    if method == 'pretty':
        pass
    #     raw_steps = SortedDict()
    #     last_marker_index = None
    #     end_marker = True
        
    #     raw_steps[min_value] = 0

    #     raw_steps[step._start] = step._weight

    #     if step._end is not None:
    #         raw_steps[step._end.start()] = 0
    #         raw_steps[max_value] = 0
    #         last_marker_index = len(raw_steps) - 2
    #     else:
    #         raw_steps[max_value] = step._weight
    #         end_marker=False

    #     _prettyplot(raw_steps,plot_start=min_value,plot_start_value=0,ax=ax,end_index=last_marker_index,include_end=end_marker,**kargs)
    elif method == 'smooth':
        ax.step(tsx,step.smooth_step(tsx,smooth_factor), where=where, **kargs)
    elif method == 'function':
        ax.step(tsx,step.step(tsx), where=where, **kargs)
    else:
        ax.step(tsx,step.step(tsx), where=where, **kargs)

    return ax