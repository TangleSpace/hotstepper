from __future__ import annotations
import numpy as np
from hotstepper.basis.Bases import Bases

class Basis(object):
    """
    This class represents a wrapper for the function to be used as the representation basis of the steps functions.

    The mathemtical base functions are contained in the Bases static abstract class and are directly referenced from the Basis class.

    All Basis assignments will only reference a Base function to improve performance and Numba compatibility.
    
    """

    def __init__(self,bfunc=None, param=1,lbound= -np.Inf,ubound = np.Inf):
        self.lbound = lbound
        self.ubound = ubound
        self.param = param
        
        if bfunc is None:
            self._base = Bases.heaviside
        else:
            self._base = bfunc
            
    def base(self):
        return self._base