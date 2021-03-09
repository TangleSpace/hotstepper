
from __future__ import annotations
import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
from pandas._libs.tslibs import NaT

from hotstepper.utilities.helpers import get_epoch_start, prepare_datetime

def to_dict(steps,cummulative_output = True):
    """
    Export steps data to a dictionary with values that represent either the cummulative value of the data steps or the direct step
    values seperately, indexed by the dictionary key values.

    Parameters
    ==============
    data : dictionary_like 
        A dictionary representing the data to convert to steps. Assumed format is:
        key    -> step start
        value  -> step weight

    use_datetime : bool, Optional = False
        Assume start and end fields are of datetime format (Numpy.datetime64,datetime or Pandas.Timestamp).

    convert_delta : bool, Optional = False
        Assume weight values are individual step weights (default), or convert values by performing a delta between adjacent values. The data
        is assumed to be sorted by the provided start values.

        Output format (cumulative)
        key   -> step index
        value -> cumulative steps value

        or

        Output format (delta)
        start : step index
        value : steps delta value between start and next index

    Returns
    ============
    Dictionary

    
    See Also
    ============
    to_array
    to_dataframe

    """

    pass


def to_dataframe(steps, cummulative_output = True):
    """
    Export steps data to a Pandas dataframe as either the step index value and cumulative value or the individual step values at each step index as keys.

    Parameters
    ==============
    steps : Steps object

    cummulative_output : bool, Optional = True
        Export cumulative value of all steps at each step index (default) or the step change (delta) value between each step index.

        Output columns (cumulative)
        start : step index
        value : cumulative steps value

        or

        Output columns (delta)
        start : step index start
        end   : step index end (next index after start)
        value : steps delta value between start and end indexes

    Returns
    ==============
    Pandas.DataFrame

    
    See Also
    ==============
    to_array
    to_dict

    """

    if steps.using_datetime():
        starts = prepare_datetime(steps.step_keys())
    else:
        starts = steps.step_keys()

    if cummulative_output:
        df = pd.DataFrame({
            'start': starts,
            'value': steps.step_values()
        })
    else:
        deltas = np.diff(steps.step_values(),prepend=0)

        df = pd.DataFrame({
            'start': starts[:-1],
            'end'  : starts[1:],
            'value': deltas
        })
        
    return df
        

#-----------------------------------inbound data readers
def read_dict(cls, data,use_datetime = False, convert_delta = True):
    """
    Read a dictionary with values that represent either the cummulative value of the data steps or the direct step
    values seperately, indexed by the dictionary key values.

    Parameters
    ==============
    data : dictionary_like 
        A dictionary representing the data to convert to steps. Assumed format is:

         - key -> step start
         - value -> step weight

    use_datetime : bool, Optional
        Assume start and end fields are of datetime format (Numpy.datetime64,datetime or Pandas.Timestamp).

    convert_delta : bool, Optional
        Assume weight values are individual step weights (default), or convert values by performing a delta between adjacent values. The data
        is assumed to be sorted by the provided start values.

    Returns
    ==============
    Steps
    
    See Also
    ==============
    read_array
    read_dataframe

    """

    if hasattr(data,'keys') and callable(data.keys) :
        return cls.read_array(list(data.keys()),None,list(data.values()),use_datetime=use_datetime,convert_delta=convert_delta)
    else:
        raise TypeError("input data must be dictionary like")


def read_dataframe(cls, data,start=None,end=None,weight=None,use_datetime = False, convert_delta = False):
    """
    Read a Pandas dataframe with values that represent either the cummulative value of the data steps or the direct step
    values seperately. 

    Parameters
    ==============
    data : Pandas.DataFrame
        A dataframe representing the data to convert to steps.

    start : str, Optional
        The name of the column containing the start data.

    end : str, Optional
        The name of the column containing the end data.

    weight : str, Optional
        The name of the column containg the step weight data, if this is not provided, a value of 1 will be assigned for each row entry.

    use_datetime : bool, Optional
        Assume start and end fields are of datetime format (Numpy.datetime64,datetime or Pandas.Timestamp).

    convert_delta : bool, Optional
        Assume weight values are individual step weights (default), or convert values by performing a delta between adjacent values. The data
        is assumed to be sorted by the provided start values.

    Returns
    ==============
    Steps
    
    See Also
    ==============
    read_array
    read_dict

    """

    if isinstance(data,pd.DataFrame):
        if start is not None:
            start = data[start]
        
        if end is not None:
            end = data[end]

        if weight is not None:
            weight = data[weight]

        return cls.read_array(start,end,weight,use_datetime,convert_delta)
    else:
        raise TypeError("input data must be a Pandas Dataframe")


def read_array(cls, start=None,end=None,weight=None,use_datetime = False, convert_delta = False):
    """
    Read arrays of values for start, end and weight values that represent either the cummulative value of the data steps or the direct step
    values seperately, indexed by the start and possibly end arrays.

    Parameters
    ==============
    start : array_like
        An array of step start location values.

    end : array_like, Optional
        An array of step end location values.

    weight : array_like, Optional
        An array of step weight values, if these are not provided, a value of 1 will be assigned for each row entry.

    use_datetime : bool, Opyional
        Assume start and end fields are of datetime format (Numpy.datetime64,datetime or Pandas.Timestamp).

    convert_delta : bool, Optional
        Assume weight values are individual step weights (default), or convert values by performing a delta between adjacent values. The data
        is assumed to be sorted by the provided start values.

    Returns
    ==============
    Steps

    See Also
    ==============
    read_dataframe
    read_dict

    """

    if hasattr(start,'__iter__') or hasattr(end,'__iter__'): #needs to be an array like object
        if convert_delta:
            weight0 = 0
            if weight[0] !=0:
                weight0 = weight[0]

            if weight0 !=0 and not pd.isnull(start[0]):
                weight = np.diff(weight)
                new_steps = cls(use_datetime).add_direct(start,end,weight)
                new_steps.add_steps([[get_epoch_start(False),1,weight0]])
            else:
                weight = np.diff(weight,prepend=0)
                new_steps = cls(use_datetime).add_direct(start,end,weight)
        else:
            new_steps = cls(use_datetime).add_direct(start,end,weight)
            
        return new_steps
    else:
        raise TypeError("input data must be array like, python array or ndarray.")

