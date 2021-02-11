import abc
import numpy as np
from hotstepper.mixins.operations import apply_math_function


class MathFunctionsMixin(metaclass=abc.ABCMeta):

    def __rfloordiv__(self,other):
        return apply_math_function(self,other,np.floor_divide)

    def __rtruediv__(self,other):
        return (self*-1)*other

    def __mod__(self,other):
        return apply_math_function(self,other,np.fmod)

    def __floordiv__(self,other):
        return apply_math_function(self,other,np.floor_divide)

    def __truediv__(self,other):
        return apply_math_function(self,other,np.true_divide)

    def __mul__(self,other):
        return apply_math_function(self,other,np.multiply)

    def __pow__(self,power_val):
        return apply_math_function(self,power_val,np.power)

    def __radd__(self,other):
        return apply_math_function(self,other,np.add)


    def __add__(self,other):
        """
        The '+' operation to add int, float, step and steps objects like they are numbers.

        Parameters
        ==============
        other : int, float, Step, Steps. The thing to add to these steps, a single step or series of steps can be combined with the steps, an single int or float can also
        be added, this will be converted to a single step with a constant basis and added to the steps series.

        Returns
        ============
        Steps : A new steps object consisting of this object with additional step objects representing the other operand.
        
        """
        return apply_math_function(self,other,np.add)


    def __rsub__(self,other):
        return -1*self + other


    def __rmul__(self,other):
        return apply_math_function(self,other,np.multiply)


    def __sub__(self,other):
        """
        The '-' operation to subtract int, float, step and steps objects like they are numbers.

        Parameters
        ==============
        other : int, float, Step, Steps. The thing to subtract from these steps, a single step or series of steps can be combined with the steps, a single int or float can also
        be added, this will be converted to a single step with a constant basis and added to the steps series.

        Returns
        ============
        Steps : A new steps object consisting of this object with additional step objects representing the other operand.
        
        """
        return apply_math_function(self,other,np.subtract)
