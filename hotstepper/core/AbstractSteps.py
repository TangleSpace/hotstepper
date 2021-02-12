from __future__ import annotations
import abc
import copy
import numpy as np
import hotstepper.analysis as analysis
import hotstepper.mixins as mixins
from hotstepper.utilities.helpers import prepare_input,get_clean_step_data
from hotstepper.core.data_model import DataModel
from hotstepper.basis.Basis import Basis
from hotstepper.basis.Bases import Bases


class AbstractSteps(metaclass=abc.ABCMeta):
    """
    The base class that defines the step object interface and base properties and methods expected of all derived classes.

    
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
    @abc.abstractmethod
    def __repr__(self):
        pass

    def compare(self,other):
        st_this_keys,st_this_values = get_clean_step_data(self)

        #check if other implements AbstractSteps interface
        if type(self).__base__ == type(other).__base__:
            st_that_keys,st_that_values = get_clean_step_data(other)
            return np.array_equal(st_this_keys, st_that_keys) and np.array_equal(st_this_values,st_that_values)
        else:
            return (st_this_values==other).all()

    def step_changes(self):
        """"
        The individual step changes at each key value, these are the delta values that add and subtract across the series to realise the entire step function.

        """

        return self._step_data[:,DataModel.DIRECTION.value]


    def first(self):
        return self._start


    def last(self):
        return self._end


    def step_values(self):
        return self._all_data[:,DataModel.WEIGHT.value]


    def step_keys(self):
        return self._all_data[:,DataModel.START.value]


    def __getitem__(self,x):
        return self.fast_step(x)


    def __call__(self,x):
        return self.fast_step(x)


    def step(self, x,process_input=True):
        """
        This is a mathematical function definition of the Steps object, this is a dynamically created formula representation that can be passed an array of values to evaluate the steps function at.
        
        """

        if process_input:
            x = prepare_input(x)

        if self._step_data.shape[0] > 0:
            result = self._base(x,self._step_data,1.0)
        else:
            return np.zeros(len(x))

        return result


    def fast_step(self,t,process_input=True):
        if process_input:
            t = prepare_input(t)

        search_data = np.concatenate([self.step(np.array([-np.inf]),False),self._all_data[:,DataModel.WEIGHT.value]])
        if self._all_data.shape[0] == 1:
            return self.step(t)

        #improves lookup performance, just need an extra check to avoid over/under run
        idxs = np.searchsorted(self._all_data[:,DataModel.START.value],t,side='right')
        return search_data[np.where(idxs>0,idxs,0)]

    def smooth_step(self,x,smooth_factor = None,smooth_basis = None):

        if smooth_factor is None:
            if self._using_dt:
                dt_factor = (self.last()-self.first()).total_seconds()/60
                smooth_factor = np.full(self._all_data.shape[0],dt_factor)
            else:
                smooth_factor = np.full(self._all_data.shape[0],10.0)

        if smooth_basis is None:
            self.rebase(new_basis=Basis(Bases.logit))
        else:
            self.rebase(new_basis=smooth_basis)

        if self._step_data.shape[0] > 0:
            st = self._step_data
            x = prepare_input(x)
            result = self._base(x*self._ts_scale,st,smooth_factor*self._ts_scale)
        else:
            return np.zeros(len(x))

        self.rebase()

        return result


    def reflect(self,reflect_point = 0):
        return self*-1 + reflect_point


    def __iter__(self):
        self._index = 0
        return iter([type(self)(self._using_dt).add_steps([s]) for s in self._step_data])


    def __next__(self):
        if self._index < self._step_data.shape[0]:
            self._index += 1
            return type(self)(self._using_dt).add_steps(self._step_data[self._index-1])
        else:
            self._index = 0
            raise StopIteration

    def __getitem__(self,x):
        return self.step(x)


    def step_data(self):
        return self._step_data


    def step_data(self):
        return self._step_data


    def using_datetime(self):
        return self._using_dt


    def copy(self):
        return copy.copy(self)


    def steps(self):
        return self._all_data

    # def rotate(self):
    #     return Steps.read_array(self.step_values(),self.step_keys(),convert_delta=True)


    def basis(self):
        return self._basis


    def rebase(self,new_basis = None):
        if new_basis is None:
            self._basis = Basis()
            self._base = self._basis.base()
        else:
            self._basis = new_basis
            self._base = new_basis.base()

    def clear(self):
        """
        Clear all the step data defined within the steps object, the same as defining a new Steps object with no data, except will retain the assigned datetime flag and base.
        """

        self._step_data = None
        self._all_data = None
        self._start = None
        self._end = None
    
#stitch in external methods
analysis.apply_mixins(AbstractSteps)
mixins.apply_mixins(AbstractSteps)
mixins.apply_classmethods(AbstractSteps)
mixins.apply_staticmethods(AbstractSteps)