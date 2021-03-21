from numba.core.decorators import njit
import numpy as np
import numba as nb
from abc import ABC


class Bases(ABC):
    """
    A static abstract class that holds the definitions for the step function and smoothing bases.

    This class is always referenced statically and therefore serves as a convenience for attaching specific base functions to the basis class.

    These methods are all Numba compiled and therefore best to be seperately out from any direct class inheritence due to performance and possible
    conflicts when copying objects with a referenced Numba function.

    The mathematical bases defined within this class are;

    Heaviside
    Logistic
    Sigmoid
    Arctan
    Exponential
    Normal
    Sinc
    
    """

    @staticmethod
    @njit(parallel=True,nogil=True)
    def heaviside(x,steps,param):
        result = np.zeros(x.shape[0])

        for i in nb.prange(steps.shape[0]):
            result += np.where(steps[i,1]*(x-steps[i,0])>=0, steps[i,2],0)

        return result


    @staticmethod
    @njit(parallel=True,nogil=True)
    def logistic(x,steps,param):
        result = np.zeros(x.shape[0])

        for i in nb.prange(steps.shape[0]):
            result += steps[i,2]*0.5*(1.0+np.tanh(steps[i,1]*(x-steps[i,0])/param))

        return result


    @staticmethod
    @njit(parallel=True,nogil=True)
    def arctan(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            result += steps[i,2]*(0.5+(1.0/np.pi)*np.arctan(steps[i,1]*(x-steps[i,0])/param))

        return result


    @staticmethod
    @njit(parallel=True,nogil=True)
    def sigmoid(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            result += steps[i,2]/(1.0+np.exp(-1*steps[i,1]*(x-steps[i,0])/param))

        return result


    @staticmethod
    @njit(parallel=True,nogil=True)
    def exponential(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            result += steps[i,2]*(np.exp(-1*np.exp(-1*steps[i,1]*(x-steps[i,0])/param)))

        return result

    @staticmethod
    @njit(parallel=True,nogil=True)
    def normal(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            result += steps[i,2]*(np.exp((-1/param)*(steps[i,1]*(x-steps[i,0]))**2))

        return result


    @staticmethod
    @njit(parallel=True,nogil=True)
    def sinc(x,steps,param):
        result = np.zeros(len(x))
            
        for i in nb.prange(steps.shape[0]):
            result += steps[i,2]*(np.sinc(steps[i,1]*(x-steps[i,0])/param))/param

        return result


