import abc
from hotstepper.utilities.helpers import step_plot
from hotstepper.mixins.StepsPlottingMixin import StepsPlottingMixin


class StepsPlottingMixin(StepsPlottingMixin,metaclass=abc.ABCMeta):

    def smooth_plot(self,smooth_factor = None, ts_grain = None,ax=None,where='post',**kargs):
        return step_plot(self,method='smooth',smooth_factor = smooth_factor,ts_grain = ts_grain,ax=ax,where=where,**kargs)


    def plot(self,method=None,smooth_factor = None,ts_grain = None,ax=None,where='post',**kargs):
        return step_plot(self,method=method,smooth_factor = smooth_factor,ts_grain = ts_grain,ax=ax,where=where,**kargs)

