from __future__ import annotations
import numpy as np
from numpy_indexed import group_by
import pandas as pd

#from docs.documentor import add_doc, append_doc
from hotstepper.core.AbstractSteps import AbstractSteps
from hotstepper.mixins.FilterFunctionsMixin import FilterFunctionsMixin
from hotstepper.mixins.MathFunctionsMixin import MathFunctionsMixin
from hotstepper.mixins.StepsPlottingMixin import StepsPlottingMixin
from hotstepper.core.data_model import DataModel
from hotstepper.utilities.helpers import (
    prepare_datetime,
    is_date_time,
    get_epoch_start,
    get_epoch_end,
    date_to_float
)


class Steps(
    StepsPlottingMixin,
    FilterFunctionsMixin,
    MathFunctionsMixin,
    AbstractSteps):


    r"""
    Class representing a complex step function made of individual step objects. The Steps object can be treated as a 
    mathemtical function in Numpy and as a Python object.

    **Terminology**
    ~~~~~~~~~~~~~~~~~
     - **start** : The x value of where the step function changes value.

     - **end** The x value where the step function changes value in the opposite direction to the start location. 

        .. note:: 
            If no start value is specified, the end location still represents the step function change in value that would have been opposite if a start been specified. In this case, the 'start' value is at negative infinity and the end location is where the reverse change occurs.

     - **weight** : The y value of the step function at the step keys.

    .. note::
        The convention used in the HotStepper library for step function intervals is the same as that used in signal processing, whereby the step function assumes the step weight value at and beyond the step key value.

    For a technical discussion of what this means, a good starting reference is `Wikipedia <https://en.wikipedia.org/wiki/Step_function>`_.
    

    Parameters
    ==============
    use_datetime : bool, Optional
        Set this value to indicate that all independant variable values (step keys), are datetime format. If the values passed as step keys
        have a callable timestamp() method or are of the accepted types below, this value will be inferred automatically, else if an error occurs,
        a good practise is to explicitly set this value.

        .. note::
            Accepted types are Pandas.Timestamp, datetime.datetime, numpy.datetime64 and any type derived from these three or exposing a callable timestamp() method returning a float or integer value os seconds since POSIX epoch.

    start : int, float, datetime_like, Optional
        A quick convenience parameter if this Steps object consists of 1 or 2 steps, the start key can be passed directly in the constructor.
        

    end : int, float, datetime_like, Optional
        A quick convenience parameter if this Steps object consists of 1 or 2 steps, the end key can be passed directly in the constructor.

    weight : int, float, Optional
        A quick convenience parameter if this Steps object consists of 1 or 2 steps, the weight is the step value.

    basis: Basis, Optional
        The is the basis function that will be used for all steps associated with this step function. The default basis -> Basis() is the Heaviside function
    
    .. math::
        :nowrap:
    
        \begin{equation*}
        \theta(t) = \left\{
                \begin{array}{ll}
                    0 & \quad t < 0 \\
                    1 & \quad t \geq 0
                \end{array}
        \right\}
        \;\;\;\;\; where \;t \in \mathbb{R}
        \end{equation*}

    """

    def __init__(self,use_datetime=False, start=None, end=None, weight=None, basis=None):
        super().__init__(use_datetime,basis)

        initialise_values_now = False

        if start is not None:
            initialise_values_now = True
            self._using_dt = self._using_dt or is_date_time(start)

        if end is not None:
            initialise_values_now = True
            self._using_dt = self._using_dt or is_date_time(end)

        if weight is not None:
            initialise_values_now = True
            weight = [weight]

        if initialise_values_now:
            self.add_direct([start],[end],weight)


    def _process_data(self,start=None,end=None,weight=None,use_datetime = False):
        start = np.full(len(end),None) if start is None else start
        weight = np.ones(len(start),dtype=np.int32) if weight is None else weight
        end = np.full(len(start),None) if end is None else end

        if use_datetime:
            convert_func = date_to_float
        else:
            convert_func = float

        epoch_start = get_epoch_start(False)
        epoch_end = get_epoch_end(False)

        for s,e,w in zip(start,end,weight):
            if pd.isnull(s) and not pd.isnull(e):
                yield (epoch_start,1,w)
                yield (convert_func(e),1,-w)
            elif pd.isnull(s) and pd.isnull(e):
                yield (epoch_start,1,w)
                yield (epoch_end,1,-w)
            elif pd.isnull(e):
                yield (convert_func(s),1,w)
            else:
                yield (convert_func(s),1,w)
                yield (convert_func(e),1,-w)


    def add_steps(self,step_data_np):
        """
        Add an array of internal step data as per the DataModel used internally by HotStepper.

        Parameters
        ==============
        step_data_np : array_like.
            Array of step arrays to be directly added to the current steps object.

        Returns
        ==============
        Steps

        """

        if step_data_np is None:
            return self

        step_data_np = np.copy(step_data_np)

        if self._step_data is None:
            self._step_data = step_data_np
        else:
            self._step_data = np.concatenate([self._step_data,step_data_np],axis=0)

        self._recalculate()
        
        return self


    def add_direct(self,data_start=None,data_end=None,data_weight=None):
        """
        Add an array of individual step objects to this collection of steps.

        Parameters
        ==============
        data_start : array_like, Optional
            Array of values that represent the step start key locations.

        data_end : array_like, Optional
            Array of values that represent the step end key locations.

        data_weight : array_like, Optional
            Array of values that represent the step values.

        .. note:: Note
            If more than one array of values are assigned, all arrays must be the same length.

        Returns
        ==============
        Steps

        """

        if data_start is not None:
            data_start = np.array(data_start)
            self._using_dt = self._using_dt or is_date_time(data_start[0])
        
        if data_end is not None:
            data_end = np.array(data_end)
            self._using_dt = self._using_dt or is_date_time(data_end[0])

        if data_weight is not None:
            data_weight = np.array(data_weight)


        if self._step_data is None:
            self._step_data = np.array(list(self._process_data(data_start,data_end,data_weight,use_datetime=self._using_dt)))
        else:
            self._step_data = np.concatenate([self._step_data,np.array(list(self._process_data(data_start,data_end,data_weight,use_datetime=self._using_dt)))],axis=0)

        self._recalculate()
        
        return self


    def add(self,steps):
        """
        Add an array of step or steps objects to this collection of steps.

        Parameters
        ==============
        steps : array_like
            An array of step or steps object.

        Returns
        ==============
        Steps
            A new steps object containing all the step data from all provided step objects.

        """

        raw_steps = np.concatenate([s.steps() for s in steps])
        raw_steps[:,DataModel.WEIGHT.value] = raw_steps[:,DataModel.DIRECTION.value]
        raw_steps[:,DataModel.DIRECTION.value] = 1

        return self.add_steps(raw_steps)


    def _recalculate(self):
        try:
            self._step_data = self._step_data[~np.isnan(self._step_data[:,DataModel.START.value])]
            #self._step_data = self._step_data[self._step_data[:,DataModel.START.value]!=0]
            self._step_data = self._step_data[self._step_data[:,DataModel.START.value]!=np.NINF]
            self._step_data = self._step_data[self._step_data[:,DataModel.START.value]!=np.PINF]
            self._step_data = self._step_data[np.argsort(self._step_data[:,DataModel.START.value])]

            #great numpy group by library! 
            all_keys,all_values = group_by(self._step_data[:,DataModel.START.value]).sum(self._step_data[:,DataModel.DIRECTION.value]*self._step_data[:,DataModel.WEIGHT.value])

            #this is the raw step definitiondata for the application of basis functions
            self._step_data = np.empty((len(all_keys),3))
            self._step_data[:,DataModel.START.value] = all_keys
            self._step_data[:,DataModel.DIRECTION.value] = 1.0
            self._step_data[:,DataModel.WEIGHT.value] = all_values

            start_key = np.amin(all_keys)
            if start_key == get_epoch_start(False):
                if len(all_keys) > 2:
                    start_key = all_keys[1]
                else:
                    start_key = all_keys[0]
            else:
                start_key = all_keys[0]

            end_key = np.amax(all_keys)
            if end_key == get_epoch_end(False) and len(all_keys) > 2:
                end_key = all_keys[-2]
            elif end_key == get_epoch_end(False) and len(all_keys) == 1:
                end_key = all_keys[0]
            else:
                end_key = all_keys[-1]

            #The real value start and end points for the entire series of steps
            self._start = start_key
            self._end = end_key

            #this is the computed summary describing the steps data for fast access
            all_data = np.empty((all_keys.shape[0],3))
            all_data[:,DataModel.START.value] = all_keys
            all_data[:,DataModel.DIRECTION.value] = all_values
            all_data[:,DataModel.WEIGHT.value] = np.cumsum(np.asarray(all_values),axis=0)

            self._all_data = all_data
            
        except ValueError:
            print('Empty steps objects can not perform operations, please load some data and try again')
        except TypeError:
            print('Empty steps objects can not perform operations, please load some data and try again')


    def clamp(self,lbound=None,ubound=None):
        """
        Clamp the steps between lower and upper limits, this function is equivalent to zeroing out the steps beyond the lower and upper limits. The returned steps will contain the specified lower and upper limit keys inclusively. 
        
        .. note:: Note
            This function will not preserve the step values at the clamp boundries, if you wish to preserve the values beyond the boundries, please use the clip function.

        Parameters
        ============
        lbound : int, float, datetime_like, Optional
            The lower step key boundry (x axis value) of the returned steps object, the exact start key of the return object will be the key value = lbound. 

        ubound : int, float, datetime_like, Optional
            The upper step key boundry (x axis value) of the returned steps object, the exact start key of the return object will be the key value = ubound. 

        See Also
        ==========
        Steps.clip

        """
        
        return self*Steps(use_datetime=self._using_dt,basis=self._basis, start=lbound,end=ubound)


    def clip(self,lbound=None,ubound=None):
        """
        Clip the steps between lower and upper limits, this function is equivalent to taking a slice of the steps and returning a new steps object only containing data between the clip boundries. The boundry values provided may or may not be returned, as the closest step key value within the specificied range will form the new boundry. 
        
        .. note:: Note
            This function will preserve the step values at the clip boundries, if you wish to zero out values beyond the boundries, please use the clamp function.

        Parameters
        ============
        lbound : int, float, datetime_like, Optional
            The lower step key boundry (x axis value) of the returned steps object, the exact start key of the return object will be the key value >= lbound. 

        ubound : int, float, datetime_like, Optional
            The upper step key boundry (x axis value) of the returned steps object, the exact start key of the return object will be the key value <= ubound. 

        See Also
        =========
        Steps.clamp

        """

        if ((lbound is not None) and (ubound is not None)) and ((lbound <= self.first()) and (ubound >= self.last())):
            return self

        if lbound is None and ubound is None:
            return self

        if self._using_dt:
            if lbound is not None:
                lbound = date_to_float(lbound)

            if ubound is not None:
                ubound = date_to_float(ubound)
        
        new_steps = self._clip(lbound,ubound)
        return Steps(self._using_dt).add_steps(new_steps)


    def _clip(self,lbound=None,ubound=None):

        step_data = self._all_data

        if lbound is None:
            lower_idx = 0
            idxs = np.searchsorted(self._all_data[:,DataModel.START.value],ubound,side='right')
            upper_idx = idxs if idxs >=0 else -1

            step_slice = step_data[:upper_idx]
            new_steps = np.empty((step_slice.shape[0],3))
            new_steps[:,DataModel.START.value] = step_slice[:,DataModel.START.value]
            new_steps[:,DataModel.DIRECTION.value] = 1
            new_steps[:,DataModel.WEIGHT.value] = step_slice[:,DataModel.DIRECTION.value]

        elif ubound is None:
            idxs = np.searchsorted(self._all_data[:,DataModel.START.value],lbound,side='right')
            lower_idx = idxs if idxs >=0 else 0
            upper_idx = -1

            step_slice = step_data[lower_idx:]
            new_steps = np.empty((step_slice.shape[0],3))
            new_steps[:,DataModel.START.value] = step_slice[:,DataModel.START.value]
            new_steps[:,DataModel.DIRECTION.value] = 1
            new_steps[:,DataModel.WEIGHT.value] = step_slice[:,DataModel.DIRECTION.value]

            new_start_weight = self(lbound)[0]
            if new_start_weight !=0:
                new_steps = np.insert(new_steps,0,[[get_epoch_start(False),1,new_start_weight]],axis=0)
            else:
                new_steps = np.insert(new_steps,0,[[lbound,1,new_start_weight]],axis=0)

        else:
            if lbound <= self._start:
                lower_idx = 0
                idxs = np.searchsorted(self._all_data[:,DataModel.START.value],ubound,side='right')
                upper_idx = idxs if idxs >=0 else -1

                step_slice = step_data[:upper_idx]
                new_steps = np.empty((step_slice.shape[0],3))
                new_steps[:,DataModel.START.value] = step_slice[:,DataModel.START.value]
                new_steps[:,DataModel.DIRECTION.value] = 1
                new_steps[:,DataModel.WEIGHT.value] = step_slice[:,DataModel.DIRECTION.value]

            elif ubound >= self._end:
                idxs = np.searchsorted(self._all_data[:,DataModel.START.value],lbound,side='right')
                lower_idx = idxs if idxs >=0 else 0
                upper_idx = -1

                step_slice = step_data[lower_idx:]
                new_steps = np.empty((step_slice.shape[0],3))
                new_steps[:,DataModel.START.value] = step_slice[:,DataModel.START.value]
                new_steps[:,DataModel.DIRECTION.value] = 1
                new_steps[:,DataModel.WEIGHT.value] = step_slice[:,DataModel.DIRECTION.value]

                new_start_weight = self(lbound)[0]
                if new_start_weight !=0:
                    new_steps = np.insert(new_steps,0,[[get_epoch_start(False),1,new_start_weight]],axis=0)
                else:
                    new_steps = np.insert(new_steps,0,[[lbound,1,new_start_weight]],axis=0)
            else:
                idxs = np.searchsorted(self._all_data[:,DataModel.START.value],lbound,side='right')
                lower_idx = idxs if idxs >=0 else 0

                idxs = np.searchsorted(self._all_data[:,DataModel.START.value],ubound,side='right')
                upper_idx = idxs if idxs >=0 else -1

                step_slice = step_data[lower_idx:upper_idx]
                new_steps = np.empty((step_slice.shape[0],3))
                new_steps[:,DataModel.START.value] = step_slice[:,DataModel.START.value]
                new_steps[:,DataModel.DIRECTION.value] = 1
                new_steps[:,DataModel.WEIGHT.value] = step_slice[:,DataModel.DIRECTION.value]

                end_val = -1*(np.sum(step_slice[lower_idx:upper_idx,DataModel.DIRECTION.value]))

                new_start_weight = self(lbound)[0]
                if new_start_weight !=0:
                    new_steps = np.insert(new_steps,0,[[get_epoch_start(False),1,new_start_weight]],axis=0)
                else:
                    new_steps = np.insert(new_steps,0,[[lbound,1,new_start_weight]],axis=0)

                new_steps = np.append(new_steps,[[ubound,1,end_val]],axis=0)

        return new_steps


    def lshift(self,other):
        """
        Left shift operator <<, used to shift the step backwards. 
        Shifts the steps keys to the left, this operation is equivalent to subtracting a constant value from all step keys. 

        Parameters
        ============
        other : int, float, timedelta_like
            The amount to subtract from all step keys. The type should align to the step key type, i.e. if the steps are using datetime, then other should be a timedelta type, else an int or float.

        See Also
        =========
        rshift

        """

        new_instance = Steps(use_datetime=self._using_dt,basis=self._basis)
        lshift_steps = np.copy(self._step_data)

        if self._using_dt:
            other = date_to_float(other)

        lshift_steps[:,DataModel.START.value] = lshift_steps[:,DataModel.START.value] - other
        return new_instance.add_steps(lshift_steps)


    def rshift(self,other):
        """
        Right shift operator >>, used to shift the step foward. 
        Shifts the steps keys to the right, this operation is equivalent to adding a constant value to all step keys. 

        Parameters
        ============
        other : int, float, timedelta_like
            The amount to addfrom all step keys. The type should align to the step key type, i.e. if the steps are using datetime, then other should be a timedelta type, else an int or float.

        See Also
        =========
        lshift

        """
        
        new_instance = Steps(use_datetime=self._using_dt,basis=self._basis)
        rshift_steps = np.copy(self._step_data)

        if self._using_dt:
            other = date_to_float(other)

        rshift_steps[:,DataModel.START.value] = rshift_steps[:,DataModel.START.value] + other
        return new_instance.add_steps(rshift_steps)


    def __lshift__(self,other):
        return self.lshift(other)


    def __rshift__(self,other):
        return self.rshift(other)


    def __repr__(self):
        if self._all_data is not None:
            if self._using_dt:
                nice_keys = prepare_datetime(self.step_keys())
            else:
                nice_keys = self.step_keys()

            nice_values = self.step_values()

            return ',\n'.join([':'.join([str(k),str(v)]) for k,v in zip(nice_keys,nice_values)])
        else:
            raise Warning('Empty Steps object')
