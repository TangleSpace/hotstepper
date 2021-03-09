from abc import ABC
import numpy as np
from hotstepper.mixins.operations import apply_math_function


class MathFunctionsMixin(ABC):

    def __rfloordiv__(self,other):
        return apply_math_function(self,other,np.floor_divide)

    def __rtruediv__(self,other):
        return (self**-1)*other

    def __mod__(self,other):
        """
        The **%** operation to take modulo int, float, step and steps objects like they are numbers.

        .. note::
            right and in-place subtraction is also available.
             - 3 - steps
             - steps -= 3
             - steps - 3

        Parameters
        ==============
        other : int, float, Step, Steps. 
            The thing to modulo against these steps, a single step or series of steps can be combined with the steps.

        Returns
        ============
        Steps
            A new steps object consisting of this object with additional step objects representing the other operand.
        
        """
        return apply_math_function(self,other,np.fmod)

    def __floordiv__(self,other):
        return apply_math_function(self,other,np.floor_divide)

    def __truediv__(self,other):
        """
        The \/ operation to divide int, float, step and steps objects like they are numbers.

        .. note::
            right and in-place division is also available.
             - 3/steps
             - steps /=3
             - steps/3

        Parameters
        ==============
        other : int, float, Step, Steps. 
            The thing to divide these steps, a single step or series of steps can be combined with the steps.

        Returns
        ============
        Steps
            A new steps object consisting of this object with additional step objects representing the other operand.
        
        """

        return apply_math_function(self,other,np.true_divide)

    def __mul__(self,other):
        """
        The \* operation to multiply int, float, step and steps objects like they are numbers.

        .. note::
            right and in-place multiplication is also available.
             - 3\*steps
             - steps \*=3
             - steps\*3

        Parameters
        ==============
        other : int, float, Step, Steps. 
            The thing to multiply these steps, a single step or series of steps can be combined with the steps.

        Returns
        ============
        Steps
            A new steps object consisting of this object with additional step objects representing the other operand.
        
        """

        return apply_math_function(self,other,np.multiply)

    def __pow__(self,power_val):
        """
        The **^** operation to raise the steps to the power of.

        Parameters
        ==============
        other : int, float, Step, Steps. 
            The thing to raise to the power of these steps, a single step or series of steps can be combined with the steps.

        Returns
        ============
        Steps
            A new steps object consisting of this object with additional step objects representing the other operand.
        
        """

        return apply_math_function(self,power_val,np.power)

    def __radd__(self,other):
        return apply_math_function(self,other,np.add)

    def __add__(self,other):
        """
        The **+** operation to add int, float, step and steps objects like they are numbers.

        .. note::
            right and in-place addition is also available.
             - 3 + steps
             - steps += 3
             - steps + 3

        Parameters
        ==============
        other : int, float, Step, Steps
            The thing to add to these steps, a single step or series of steps can be combined with the steps.

        Returns
        ============
        Steps
            A new steps object consisting of this object with additional step objects representing the other operand.
        
        """

        return apply_math_function(self,other,np.add)


    def __rsub__(self,other):
        return -1*self + other


    def __rmul__(self,other):
        return apply_math_function(self,other,np.multiply)


    def __sub__(self,other):
        """
        The **-** operation to subtract int, float, step and steps objects like they are numbers.

        .. note::
            right and in-place subtraction is also available.
             - 3 - steps
             - steps -= 3
             - steps - 3

        Parameters
        ==============
        other : int, float, Step, Steps. 
            The thing to subtract from these steps, a single step or series of steps can be combined with the steps.

        Returns
        ============
        Steps
            A new steps object consisting of this object with additional step objects representing the other operand.
        
        """

        return apply_math_function(self,other,np.subtract)
