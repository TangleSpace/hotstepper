from numba.core.decorators import njit
import numpy as np
import numba as nb
import abc


class Bases(metaclass=abc.ABCMeta):
    """
    A static abstract class that holds the definitions for the step function and smoothing bases.

    This class is always referenced statically and therefore serves as a convenience for attaching specific base functions to the basis class.

    These methods are all Numba compiled and therefore best to be seperately out from any direct class inheritence due to performance and possible
    conflicts when copying objects with a referenced Numba function.

    The mathematical bases defined within this class are;

    Heaviside
    Logit
    Sigmoid
    Arctan
    Exponential
    Sinc
    
    """

    @staticmethod
    @njit(parallel=True,nogil=True)
    def heaviside(x,steps,param):
        result = np.zeros(x.shape[0])

        for i in nb.prange(steps.shape[0]):
            input = (x-steps[i,0])
            input[np.isnan(input)] = 0
            result += np.where(steps[i,1]*input>=0, steps[i,2],0)

        return result


    @staticmethod
    @njit(parallel=True,nogil=True,fastmath=True)
    def logit(x,steps,param):
        result = np.zeros(x.shape[0])

        for i in nb.prange(steps.shape[0]):
            input = (x-steps[i,0])
            input[np.isnan(input)] = 0
            result += steps[i,2]*0.5*(1.0+np.tanh(steps[i,1]*input/param))

        return result


    @staticmethod
    @njit(parallel=True,nogil=True,fastmath=True)
    def arctan(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            input = (x-steps[i,0])
            input[np.isnan(input)] = 0
            result += steps[i,2]*(0.5+(1.0/np.pi)*np.arctan(steps[i,1]*input/param))

        return result

    @staticmethod
    @njit(parallel=True,nogil=True,fastmath=True)
    def sigmoid(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            input = (x-steps[i,0])
            input[np.isnan(input)] = 0
            result += steps[i,2]/(1.0+np.exp(-1*steps[i,1]*input/param))

        return result

    @staticmethod
    @njit(parallel=True,nogil=True,fastmath=True)
    def expon(x,steps,param):
        result = np.zeros(len(x))

        for i in nb.prange(steps.shape[0]):
            input = (x-steps[i,0])
            input[np.isnan(input)] = 0
            result += steps[i,2]*(1.0 - np.exp(-1*steps[i,1]*input/param))

        return result


    @staticmethod
    @njit(parallel=True,nogil=True,fastmath=True)
    def sinc(x,steps,param):
        result = np.zeros(len(x))
            
        for i in nb.prange(steps.shape[0]):
            input = (x-steps[i,0])
            input[np.isnan(input)] = 0
            result += steps[i,2]*np.sinc(-1*steps[i,1]*input/param)

        return result


