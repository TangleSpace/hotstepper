from __future__ import annotations
#import abc
from abc import ABC, abstractmethod 
import copy
import numpy as np
import pandas as pd
import hotstepper.analysis as analysis
import hotstepper.mixins as mixins
from hotstepper.core.data_model import DataModel
from hotstepper.basis.Basis import Basis
from hotstepper.basis.Bases import Bases

from hotstepper.utilities.helpers import (
    get_epoch_start,
    get_epoch_end,
    prepare_input,
    get_clean_step_data,
    prepare_datetime,
    process_slice,
    get_datetime)



class AbstractSteps(ABC):
    """
    The base class that defines the steps object interface, base properties and methods expected of all derived classes.

    
    """

    __slots__ = ('_start','_using_dt','_end','_basis','_base','_step_data','_ts_scale','_all_data')
    
    def __init__(self,use_datetime=False,basis=None):
        super().__init__()
        self._step_data = None
        self._all_data = None
        if basis is None:
            basis = Basis()

        self._basis = basis
        self._using_dt = use_datetime
        self._base = basis.base()

        self._ts_scale = 1

    # Expected methods of parent classes
    @abstractmethod
    def __repr__(self):
        pass

    def compare(self,other):
        """
        Compare the steps function with another to determine if the two are equivalent based on their cummulative values and step keys.

        Parameters
        ===========
        other : AbstractSteps
            The other steps object to come this one to

        Returns
        ========
        bool
            Indication if the two steps a equivalent or not.

        """
        
        st_this_keys = self.step_keys()
        st_this_values = self.step_values()

        #check if other implements AbstractSteps interface
        if type(self).__base__ == type(other).__base__:
            st_that_keys = other.step_keys()
            st_that_values = other.step_values()
            return np.array_equal(st_this_keys, st_that_keys) and np.array_equal(st_this_values,st_that_values)
        else:
            return (st_this_values==other).all()


    def step_data(self,delta_values=False,convert_keys=False):
        """
        A clean multi-dimensional numpy array of the step keys and either the cummulative values or the step change values all in floats and ready to use in further analysis.
        
        .. note::
            This function returns a dataset that can directly be consumed by numpy, Sklearn and similar packages for forecasting or analysis.


        Parameters
        ===========
        delta_values : bool, Optional
            Return the step delta changes instead of the cummulative total at each step key.

        convert_keys : bool Optional
            If the keys are datetime, they will be converted, else they will remain floats.


        Returns
        ========
        array


        """

        if delta_values:
            nice_data = np.copy(self._all_data[:,[DataModel.START.value,DataModel.DIRECTION.value]])
        else:
            nice_data = np.copy(self._all_data[:,[DataModel.START.value,DataModel.WEIGHT.value]])

        if nice_data[0,DataModel.START.value] == get_epoch_start(False):
            nice_data = nice_data[1:]

        if nice_data[-1,DataModel.START.value] == get_epoch_end(False):
            nice_data = nice_data[:-1]

        if convert_keys and self._using_dt:
            nice_data = np.array(list(zip(prepare_datetime(nice_data[:,DataModel.START.value]),nice_data[:,DataModel.DIRECTION.value])))

            if nice_data[0,DataModel.START.value] == get_epoch_start():
                nice_data[0,DataModel.START.value] = nice_data[1,DataModel.START.value]
        else:
            return self._all_data[:,DataModel.START.value]

        return nice_data


    def iloc(self,idx,raw_keys=True):
        """
        The individual step changes at each array index, these are the delta values that add and subtract across the series to realise the entire step function.

        Parameters
        ============
        idx : int, slice
            The numpy index, range index or slice to lookup the raw step change values wihtin the Steps DataModel

        Returns
        ========
        array
            Individual step change values within the steps object.

        """

        nice_data = np.copy(self._all_data[idx,[DataModel.START.value,DataModel.DIRECTION.value,DataModel.WEIGHT.value]])

        return nice_data


    def step_changes(self):
        """
        The individual step changes at each key value, these are the delta values that add and subtract across the series to realise the entire step function.


        Returns
        ========
        array
            Individual step change values within the steps object.

        """

        return self._all_data[:,DataModel.DIRECTION.value]


    def first(self):
        """
        The first key or start value of the steps, if the steps extend to negative infinity, the first value will be the first finite key value.

        Returns
        ========
        int, float or datetime
            First finite key value of the steps.

        """
        if self._using_dt:
            return get_datetime(self._start)

        return self._start


    def last(self):
        """
        The last key or start value of the steps, if the steps extend to positive infinity, the last value will be the last finite key value.

        Returns
        ========
        int, float or datetime
            Last finite key value of the steps.

        """

        if self._using_dt:
            return get_datetime(self._end)

        return self._end


    def step_values(self):
        """
        The cummulative step values at each key value.


        Returns
        ========
        array
            Cummulative steps value at each step key within the steps object

        """

        return self._all_data[:,DataModel.WEIGHT.value]


    def step_keys(self,convert_keys=False):
        """
        The step key values within this object, can be returned either in raw float format or converted if using datetime.

        Parameters
        ===========
        convert_keys : bool Optional
            If the keys are datetime, they will be converted, else they will remain floats.


        Returns
        ========
        array
            Step keys

        """

        if convert_keys and self._using_dt:
            keys = prepare_datetime(self._all_data[:,DataModel.START.value],self._using_dt)
            if keys[0] == get_epoch_start():
                keys[0] = keys[1]
            
            return keys
        else:
            return self._all_data[:,DataModel.START.value]


    def __getitem__(self,x):
        x = process_slice(x)
        return self.fast_step(x)


    def __call__(self,x):
        return self.fast_step(x)


    def step(self, xdata,process_input=True):
        """
        This is a mathematical function definition of the Steps object, this is a dynamically created formula representation that can be passed an array of values to evaluate the steps function at.
        
        Parameters
        ===========
        xdata : array_like(int, float, datetime)
            The values the steps function is the be evaluated at using the assigned mathematical basis function.

        process_input : bool, Optional
            Indicate if the input data needs processing, to convert datetimes to floats for calculation. Primarily used internally to avoid converting input data twice.

        Returns
        ========
        array
            The values of the cummulative steps function evaluated at the provided input (x axis) values.

        See Also
        =========
        fast_step
        smooth_step

        """

        #if we are using default basis, get answer even quicker
        # if self._basis.name == 'Heaviside' and self._all_data.shape[0] != 1:
        #     return self.fast_step(xdata=xdata,process_input=process_input)

        if process_input:
            x = prepare_input(xdata)
        else:
            x = xdata

        if self._step_data.shape[0] > 0:
            result = self._base(x,self._step_data,self._basis.param)
            if (self._basis.name != 'Heaviside') and (x[0] == get_epoch_start(False)):
                result[0] = result[1] 
        else:
            return np.zeros(len(x))

        return result


    def fast_step(self,xdata,process_input=True,side='right'):
        """
        This will evaluate the cummulative steps function at the provided input values. This function ignores the assigned basis and performs some numpy trickery to improve performance.
        
        .. note::
            This function will ignore the assigned basis and evaluate the cummulative function directly, to ensure the assigned basis is used, please use the `step` function.

        
        Parameters
        ==========
        xdata : array_like(int, float, datetime)
            The values the steps function is to be evaluated at.

        process_input : bool, Optional
            Indicate if the input data needs processing, to convert datetimes to floats for calculation. Primarily used internally to avoid converting input data twice.

        side : {'right', 'left'}, Optional
            Location to evaluate the steps function relative to the step location. Default is *'right'*, which means the step assumes the weight value on and after the step key value.

        Returns
        ========
        array
            The values of the cummulative steps function evaluated at the provided input (x axis) values.

        See Also
        =========
        step
        smooth_step

        """

        if process_input:
            x = prepare_input(xdata)
        else:
            x = xdata

        search_data = np.concatenate([self.step(np.array([get_epoch_start(False)]),False),self._all_data[:,DataModel.WEIGHT.value]])
        if self._all_data.shape[0] < 5:
            return self.step(x)

        #improves lookup performance, just need an extra check to avoid over/under run
        limit = search_data.shape[0]
        idxs = np.searchsorted(self._all_data[:,DataModel.START.value],x,side=side)
        return search_data[np.clip(idxs,0,limit)]


    def smooth_step(self,xdata,smooth_factor = None,smooth_basis = None, process_input = True):
        """
        This is a mathematical function definition of the Steps object, this is a dynamically created formula representation that can be passed an array of values to evaluate the steps function at.
        If a basis other than the default (Heaviside) is assigned and no new basis is provided, this function will return the same result as a call to the `step` function. If the default basis is assigned, and no new
        basis is provided, the Logit basis will be temporarily assigned, the result generated and the basis will be reset to the default.

        Parameters
        ==========
        xdata : array_like(int, float, datetime)
            The values the steps function is the be evaluated at using the assigned mathematical basis function.

        smooth_factor : int, float, Optional
            A value used to tune the strength of the smoothing for the assigned basis. If no value is provided, a value will be generated internally.

        smooth_basis : Basis, Optional
            The new basis to assigned to perform the smoothing with. If the provided basis has the default value for the param property, a value will be generated internally.

        process_input : bool, Optional
            Indicate if the input data needs processing, to convert datetimes to floats for calculation. Primarily used internally to avoid converting input data twice.

        Returns
        ========
        array
            The values of the cummulative steps function evaluated at the provided input (x axis) values using the smooth basis.

        See Also
        =========
        step
        fast_step

        """

        using_default = self._basis.name == 'Heaviside'
        #check we don't already have a new basis assigned
        if using_default:
            

            if smooth_basis is None:
                if smooth_factor is None:
                    smooth_factor = self._get_auto_smooth_factor()
                self.rebase(new_basis=Basis(Bases.logistic,param=smooth_factor))
            else:
                # Override basis param is we got smooth_factor
                if smooth_factor is not None:
                    smooth_basis.param = smooth_factor
                    #smooth_factor = self._get_auto_smooth_factor()

                self.rebase(new_basis=smooth_basis)

        if self._step_data.shape[0] > 0:
            if process_input:
                x = prepare_input(xdata)
            else:
                x = xdata
            result = self._base(x,self._step_data,self._basis.param)
        else:
            return np.zeros(len(xdata))

        if using_default:
            self.rebase()

        return result

    def _get_auto_smooth_factor(self):
        delta = self.last()-self.first()
        step_length = self._step_data.shape[0]
        if self._using_dt and delta !=0:
            return (delta).total_seconds()/60
        else:
            #fiddle for a pretty smooth curve
            if step_length == 1:
                return 0.25
            elif step_length <= 4:
                return (delta/5.0)
            else:
                return 10.0


    def reflect(self,reflect_point = 0):
        return self*-1 + reflect_point


    def __iter__(self):
        
        if self._step_data[0,DataModel.START.value] == get_epoch_start(False):
            self._index = 1
            return iter([type(self)(self._using_dt).add_steps([s]) for s in self._step_data[1:]])
        else:
            self._index = 0
            return iter([type(self)(self._using_dt).add_steps([s]) for s in self._step_data])


    def __next__(self):
        if self._index < self._step_data.shape[0]:
            self._index += 1
            return type(self)(self._using_dt).add_steps([self._step_data[self._index-1]])
        else:
            self._index = 0
            raise StopIteration


    def using_datetime(self):
        """
        Check if this steps object is using datetime step keys or not.

        Returns
        =======
        bool

        """
        
        return self._using_dt


    def copy(self):
        """
        Return a shallow copy of this steps object

        Returns
        =======
        Steps

        """
        return copy.copy(self)


    def steps(self):
        """
        Return all the raw steps data within this steps object.
        The format follows the internal `hotstepper.core.data_model`.

        array
            array
                step_key,
                step_delta,
                step_cummulative


        Returns
        ========
        array(array)

        See Also
        ========
        core.DataModel

        """
        
        return self._all_data


    def series(self,xdata=None,ydata=None):
        """
        A convenience function to either return the internal steps data in a Pandas Series object with the steps keys as the index or convert a provided 2-D set of data into a Pandas Series.

        The Pandas Series has a number of helpful methods and features and the ability to quickly convert 2-D data into a Pandas Series allows for fast iteration during analysis.

        Parameters
        ============
        xdata : array_like, tuple, Optional
            A 1-D array representing the data to use as the index of the Pandas Series or,
            A tuple representing 2 x 1-D arrays to use as the index and values of the Pandas Series.

        ydata : array_like, Optional
            A 1-D array represeting the data to use as the values of the Pandas Series. If no xdata is provided, an integer based index will be generated across the length of the provided ydata.

        Returns
        ========
        Pandas.Series
        
        """
        
        if ydata is None and xdata is None:
            xdata, ydata = get_clean_step_data(self)

            if self.using_datetime():
                xdata = prepare_datetime(xdata)

        elif ydata is None and xdata is not None:
            if isinstance(xdata,tuple):
                ydata = xdata[1]
                xdata = xdata[0]           
            else:
                ydata = xdata
                xdata = list(range(len(ydata)))

        return pd.Series(
                data=ydata,
                index=pd.Index(xdata)
                )

    # def rotate(self):
    #     return Steps.read_array(self.step_values(),self.step_keys(),convert_delta=True)


    def basis(self):
        """
        Return a reference to the assigned `Basis`.

        Returns
        =======
        Basis

        """
        
        return self._basis


    def rebase(self,new_basis = None):
        """
        Change the basis function to apply to the steps data when evaluating as a mathematical function, the default basis is the Heaviside step function.

        Parameters
        ===========
        new_basis : Basis
            The new basis to assign to the steps function. If the provided Basis is None, the basis will be reset to the default of the Heaviside function.


        .. note::
            If the new basis has the default value for the param property, an internally generated value will be assigned.

        """
        
        if new_basis is None:
            self._basis = Basis()
            self._base = self._basis.base()
        else:
            self._basis = new_basis
            self._base = new_basis.base()
            if self._basis.name != 'Heaviside' and self._basis.param == 1.0:
                self._basis.param = self._get_auto_smooth_factor()


    def clear(self):
        """
        Clear all the step data defined within the steps object, the same as defining a new Steps object with no data, except will retain the assigned datetime flag and base.
        
        """

        self._step_data = None
        self._all_data = None
        self._start = None
        self._end = None
        self._basis = Basis()
        self._base = self._basis.base()
    
#stitch in external methods
analysis.apply_mixins(AbstractSteps)
mixins.apply_mixins(AbstractSteps)
mixins.apply_classmethods(AbstractSteps)
mixins.apply_staticmethods(AbstractSteps)