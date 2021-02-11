import numpy as np
import scipy.linalg as spl

class Sequency():
    
    def __init__(self):
        pass
    
    def get_sequency(self,input_array:np.ndarray) -> int:

        input_shift = np.roll(input_array,1)
        input_shift[0]= 0
        diffs = input_array + input_shift
        return np.sum(np.where(diffs==0,1,0))

    def get_walsh_matrix(self,n:int,dtype=int)-> np.ndarray:
        hadamard = spl.hadamard(n,dtype=dtype)
        sequencies = np.apply_along_axis(self.get_sequency, 1, hadamard)
        return np.sort(sequencies),hadamard[np.argsort(sequencies)]

    def get_walsh_transform(self,input_values: np.ndarray, pad_mode=None, **kargs) -> np.ndarray:

        l = len(input_values)
        scale = 2**(int(np.trunc(np.log2(l))))

        if pad_mode is not None and l % scale != 0:
            scale *= 2
            input_values = np.pad(input_values,(0,scale - l),pad_mode,**kargs)

        input_scaled = input_values[:scale]
        seq, wm = self.get_walsh_matrix(scale)
        wt = np.dot(wm,input_scaled)/scale

        if pad_mode is not None and l % scale != 0:
            return seq[:l], wt[:l]
        else:
            return seq, wt

    def get_inverse_walsh_transform(self,input_values: np.ndarray, pad_mode=None,**kargs) -> np.ndarray:

        l = len(input_values)
        scale = 2**(int(np.trunc(np.log2(l))))

        if pad_mode is not None and l % scale != 0:
            scale *= 2
            input_values = np.pad(input_values,(0,scale - l),pad_mode,**kargs)

        input_scaled = input_values[:scale]

        seq, wm = self.get_walsh_matrix(scale)
        iwt = np.dot(wm,input_scaled)

        if pad_mode is not None and l % scale != 0:
            return seq[:l], iwt[:l]
        else:
            return seq, iwt

    def get_sequency_power_spectrum(self, input_values:np.ndarray,pad_mode=None,**kargs) -> np.ndarray:

        s,w = self.get_walsh_transform(input_values,pad_mode=None,**kargs)
        return s, np.power(w,2)/(np.sum(np.power(w,2)))
