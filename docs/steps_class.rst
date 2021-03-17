==============
Steps class
==============

Class representing a complex step function made of individual step objects. The Steps object can be treated as a 
mathemtical function in Numpy and as a Python object.


Terminology
===============
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
    The basis function that will be used for all step data associated with this steps object. The default basis -> Basis() is the Heaviside function

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