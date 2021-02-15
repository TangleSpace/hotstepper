import abc
import operator
from hotstepper.mixins.operations import filter_values


class FilterFunctionsMixin(metaclass=abc.ABCMeta):

    def __neg__(self):
        return self*-1
        
    def __gt__(self,other):
        return filter_values(self,other, operator.gt)
    
    def __lt__(self,other):
        return filter_values(self,other, operator.lt)

    def __ge__(self,other):
        return filter_values(self,other, operator.ge)
    
    def __le__(self,other):
        return filter_values(self,other, operator.le)

    def __ne__(self,other):
        return filter_values(self,other, operator.ne)

    def normalise(self,normalise_value = 1):
        """
        Create new steps with a constant weight of 1 everywhere the steps are not equal to zero.

        Parameters
        ==============
        normalise_value : int, float, Optional 
            The value the constant weight will be set to where the steps are not equal to zero.

        Returns
        ============
        Steps
        
        """

        return filter_values(self,0, operator.ne,normalise_value=normalise_value)

    def invert(self,normalise_value = 1):
        """
        Create new steps with a constant weight of 1 everywhere the steps are equal to zero.

        Parameters
        ==============
        normalise_value : int, float, Optional 
            The value the constant weight will be set to where the steps are equal to zero.

        Returns
        ============
        Steps
        
        """

        return filter_values(self,0, operator.eq,normalise_value=normalise_value)

    def __invert__(self):
        return self.invert()

    def __eq__(self,other):
        return filter_values(self,other, operator.eq)