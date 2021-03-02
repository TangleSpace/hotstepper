==============
Basis and Bases
==============

Basis
=========

    This class represents a wrapper for the function to be used as the representation basis of the steps functions.
    The mathemtical base functions are contained in the Bases static abstract class and are directly referenced from the Basis class.
    All Basis assignments will only reference a Base function to improve performance and Numba compatibility.
    
    Parameters
    ==============
    bfunc : numpy.ufunc, Optional
        This is the function as selected from the static method in the Bases class.

        .. note::
            You can define your own basis function by creating a numpy ufunc and passing that in, however it must follow the parameter specifications perscribed by the Bases function interfaces.

    param : float, Optional
        This will control the strength of the applied smoothing base function as per the one parameter specification.

        .. note::
            This parameter doesn't do anything for the Heaviside basis, as this is not a smoothing basis.

    name : str, Optional
        A name to reference the assigned base function with, this is used internally to check is using function from the Bases class or a custom and the nature of the function, smoothing or not.


    Methods
    ==========
    base : 
        Returns a reference to the assigned base function that is directly callable for evaluation.


Bases
=========

    A static abstract class that holds the definitions for the step function and smoothing bases.

    This class is always referenced statically and therefore serves as a convenience for attaching specific base functions to the basis class.

    These methods are all Numba compiled and therefore best to be seperately out from any direct class inheritence due to performance and possible
    conflicts when copying objects with a referenced Numba function.

    The mathematical bases defined within this class are;

     - Heaviside
     - Logit
     - Sigmoid
     - Arctan
     - Exponential
     - Sinc

