from abc import ABC
import operator
from hotstepper.mixins.operations import filter_values


class FilterFunctionsMixin(ABC):

    def __neg__(self):
        """
        Equivalent to multiplying the Steps by -1.

        Returns
        ========
        Steps

        """

        return self*-1
        
    def __gt__(self,other):
        """
        Greater than boolean comparison.
        Returns a new Steps object where the cummulative steps function is > to the filter parameter.

        Parameters
        ===========
        other : int, float, Step, Steps
            The value or steps object to compare the values of this steps object with. If the filter parameter is a different length to the steps object, the filter parameter will be broadcast across the steps and where the condition is true, the values will be returned.

        Returns
        ========
        Steps

        """
        
        return filter_values(self,other, operator.gt)
    
    def __lt__(self,other):
        """
        Less than boolean comparison.
        Returns a new Steps object where the cummulative steps function is < to the filter parameter.

        Parameters
        ===========
        other : int, float, Step, Steps
            The value or steps object to compare the values of this steps object with. If the filter parameter is a different length to the steps object, the filter parameter will be broadcast across the steps and where the condition is true, the values will be returned.

        Returns
        ========
        Steps

        """
        return filter_values(self,other, operator.lt)

    def __ge__(self,other):
        """
        Greater than or equal to boolean comparison.
        Returns a new Steps object where the cummulative steps function is >= to the filter parameter.

        Parameters
        ===========
        other : int, float, Step, Steps
            The value or steps object to compare the values of this steps object with. If the filter parameter is a different length to the steps object, the filter parameter will be broadcast across the steps and where the condition is true, the values will be returned.

        Returns
        ========
        Steps

        """

        return filter_values(self,other, operator.ge)
    
    def __le__(self,other):
        """
        Less than or equal to boolean comparison.
        Returns a new Steps object where the cummulative steps function is <= to the filter parameter.

        Parameters
        ===========
        other : int, float, Step, Steps
            The value or steps object to compare the values of this steps object with. If the filter parameter is a different length to the steps object, the filter parameter will be broadcast across the steps and where the condition is true, the values will be returned.

        Returns
        ========
        Steps

        """
        return filter_values(self,other, operator.le)

    def __ne__(self,other):
        """
        Not equal to boolean comparison.
        Returns a new Steps object where the cummulative steps function is != to the filter parameter.

        Parameters
        ===========
        other : int, float, Step, Steps
            The value or steps object to compare the values of this steps object with. If the filter parameter is a different length to the steps object, the filter parameter will be broadcast across the steps and where the condition is true, the values will be returned.

        Returns
        ========
        Steps

        """
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
        """
        Equal to boolean comparison.
        Returns a new Steps object where the cummulative steps function is == to the filter parameter.

        Parameters
        ===========
        other : int, float, Step, Steps
            The value or steps object to compare the values of this steps object with. If the filter parameter is a different length to the steps object, the filter parameter will be broadcast across the steps and where the condition is true, the values will be returned.

        Returns
        ========
        Steps

        """
        
        return filter_values(self,other, operator.eq)