from __future__ import annotations
from hotstepper.Steps import Steps
from hotstepper.basis.Basis import Basis
#from hotstepper.mixins.StepPlottingMixin import StepPlottingMixin
from hotstepper.utilities.helpers import is_date_time,step_plot


class Step(Steps):
    

    def __init__(self, start=None, end = None, weight = None, basis = Basis(), use_datetime = False):
        super().__init__(use_datetime=use_datetime,basis=basis)
        
        if start is not None:
            self._using_dt = self._using_dt or is_date_time(start)

        if end is not None:
            self._using_dt = self._using_dt or is_date_time(end)

        #if start is not None or end is not None:
        self._process_parameters(start,end,weight)


    def _process_parameters(self,start=None,end=None,weight=None,use_datetime = False):
        if weight is not None:
            weight = [weight]
        self.add_direct([start],[end],weight)

