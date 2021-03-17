import numpy as np
import scipy.linalg as spl

class Sequency():
    
    def __init__(self):
        pass
    
    def _get_sequency(self,input_array):

        input_shift = np.roll(input_array,1)
        input_shift[0]= 0
        diffs = input_array + input_shift
        return np.sum(np.where(diffs==0,1,0))


    def walsh_matrix(self,scale):
        """
        Generate sequency order Walsh functions and return in a matrix.

        Parameters
        ==============
        scale : int
            The length of the Walsh functions, must be a power of 2, else will raise an exception.

            .. note::
                A scale = 8 means each Walsh function will have 8 data points and therefore be 8 units in length.

        Returns
        ============
        tuple(array, array(scale x scale))
            sequencies, scale x scale matrix of Walsh functions

        """
        
        hadamard = spl.hadamard(scale,dtype=int)
        sequencies = np.apply_along_axis(self._get_sequency, 1, hadamard)
        return np.sort(sequencies),hadamard[np.argsort(sequencies)]


    def fwt(self,input_values,basis_span='post',pad_mode='constant', **kargs):
        """
        Perform a Fast Discrete Walsh Transform on the input data. This will decompose the data using Walsh basis functions and create a vector of
        weighting values that represent the amplitude of each Walsh basis within the data. This is the discrete step decomposition equivalent of
        a Discrete Fast Fourier Transform, whereby the Sine and Cosine basis functions are replaced by Walsh functions.

        Parameters
        =============
        input_values : array_like
            The data to be decomposed via Walsh functions.

        basis_span : {'post','pre'}, Optional
            How long the Walsh basis functions should be relative to the input data.
             - **post** will extend the Walsh basis to the next length beyond the input data length that is a power of 2.
             - **pre** will truncate the Walsh basis to the next length less than the input data length that is a power of 2.

        pad_mode : {None, 'edge','constant'}, Optional
            This is how the input data is to be padded to match the requirement of each Walsh basis being a length which is a power of 2.

            .. note::
                The allowable parameters are the same as those for the Numpy.pad function and therefore any valid mode string or function
                can be used here and it will be passed to the Numpy.pad function.
                
        kargs : any
            Key-value arguments that will be passed to the Numpy.pad function, please see the Numpy.pad documentation for further details of
            allowable kargs for this function.

        Returns
        ==========
        tuple(array, array, int)
            sequencies, spectrum_amplitudes, walsh function range

        See Also
        ==========
        Sequency.fft

        References
        ==========
        .. https://mathworld.wolfram.com/WalshTransform.html

        """

        l = len(input_values)

        if basis_span == 'post':
            scale = 2**(1 + int(np.trunc(np.log2(l))))
        else:
            scale = 2**(int(np.trunc(np.log2(l))))

        if l % scale != 0 and scale > l:
            input_scaled = np.pad(input_values,(0,scale - l),pad_mode, **kargs)
        else:
            input_scaled = input_values[:scale]

        sf, wm = self.walsh_matrix(scale)
        wt = np.dot(wm,input_scaled)/scale

        return sf, wt,scale


    def ifwt(self,fwt_data, scale=None, return_length=None):
        """
        Perform an inverse Fast Discrete Walsh Transform on the input data. The input data is expected to be an array representing the transform amplitudes from a Walsh transform of a dataset.
        This method will use the amplitude data to reconstruct the original dataset using the provided ammplitudes matrix. The scale of the Walsh basis functions can be specified explcitly using the **scale** parameter, else if 
        this parameter is not explicitly set, the scale value will be derived from the length of the fwt_data (amplitude) array.


        Parameters
        ==============
        fwt_data : array_like
            The Walsh transform amplitudes to use to reconstruct the dataset.

        scale : int, Optional
            The scale (length) of the Walsh functions to use when performing the inverse Walsh transform.

            .. note::
                This value must be a multiple of 2 or an exception will be raised.


        return_length : int, Optional
            The length of the reconstructed dataset, as the length of the original data may not be a multiple of 2, the scale of the Walsh functions used in thr transform (fwt) method may be shorter or longer, therefore when returning a reconstruction, you can specify a length to truncate the reconstuction at.


        Returns
        ==========
        array
            reconstructed dataset

        References
        =============
        .. https://mathworld.wolfram.com/WalshTransform.html

        """

        if scale is None:
            scale = len(fwt_data)

        _, wm = self.walsh_matrix(scale)
        iwt = np.dot(wm,fwt_data[:scale])

        if return_length is None:
            return iwt
        else:
            return iwt[:return_length]


    def denoise(self,input_values,method='walsh', basis_span='post',pad_mode='constant', denoise_mode='value',denoise_strength=0.5):
        """
        Perform a denoise operation on the input_values using either Walsh or Fourier method.

        Parameters
        ============
        input_values : array_like
            The data to be denoised via Walsh transform.

        method : {'walsh', 'fourier}, Optional
            The denoise method to apply to the data.
             - **walsh**, use a Walsh decomposition to produce the components to modify for denoising.
             - **fourier**, use a Fourier decomposition to produce the components to modify for denoising.

        basis_span : {'post','pre'}, Optional
            How long the Walsh basis functions should be relative to the input data.
             - **post** will extend the Walsh basis to the next length beyond the input data length that is a power of 2.
             - **pre** will truncate the Walsh basis to the next length less than the input data length that is a power of 2.

        pad_mode : {None, 'edge','constant'}, Optional
            This is how the input data is to be padded to match the requirement of each Walsh basis being a length which is a power of 2.

            .. note::
                The allowable parameters are the same as those for the Numpy.pad function and therefore any valid mode string or function
                can be used here and it will be passed to the Numpy.pad function.
        
        denoise_mode : {'range', 'value'}, Optional
            The type of filtering to use.
             - **range** will remove a proportion of the higher sequency/frequency components based on the denoise_strength value.
             - **value** will remove the sequency/frequency components that are below the value based on the denoise_strength.


        denoise_strength : float, Optional
            The strength of the denoising, this parameter controls how the components are altered in order to denoise the input_data.

        Returns
        =============
        array
            denoised data

        """

        if method == 'walsh':
            return self._walsh_denoise(input_values=input_values,basis_span=basis_span,pad_mode=pad_mode, denoise_mode=denoise_mode,denoise_strength=denoise_strength)
        else:
            return self._fourier_denoise(input_values=input_values,denoise_mode=denoise_mode,denoise_strength=denoise_strength)


    def _walsh_denoise(self,input_values,basis_span='post',pad_mode='constant', denoise_mode='value',denoise_strength=0.5):
        """
        Perform a Fast Discrete Walsh Transform on the input data, selectively removing sequency components by setting their amplitudes to zero, then reconstruct the original dataset by performing an inverse Walsh transform on the remaining amplitudes.
        

        Parameters
        ============
        input_values : array_like
            The data to be denoised via Walsh transform.

        basis_span : {'post','pre'}, Optional
            How long the Walsh basis functions should be relative to the input data.
             - **post** will extend the Walsh basis to the next length beyond the input data length that is a power of 2.
             - **pre** will truncate the Walsh basis to the next length less than the input data length that is a power of 2.

        pad_mode : {None, 'edge','constant'}, Optional
            This is how the input data is to be padded to match the requirement of each Walsh basis being a length which is a power of 2.

            .. note::
                The allowable parameters are the same as those for the Numpy.pad function and therefore any valid mode string or function
                can be used here and it will be passed to the Numpy.pad function.
        
        denoise_mode : {'range', 'value'}, Optional
            The type of filtering to use.
             - **range** will remove a proportion of the higher sequency components based on the denoise_strength value.
             - **value** will remove the sequency components that are below the value based on the denoise_strength.


        denoise_strength : float, Optional
            The strength of the denoising, this parameter controls how the components are altered in order to denoise the input_data.

        Returns
        =============
        array
            denoised data

        """

        l = len(input_values)

        _,wt,sc = self.fwt(input_values=input_values,basis_span=basis_span,pad_mode=pad_mode)

        if denoise_strength >= 0 and denoise_strength < 1:
            if denoise_mode == 'range':
                filter_idx = int(denoise_strength*sc)
                wt[-filter_idx:] = 0
            else:
                denoise_threshold = np.amax(np.absolute(wt))*denoise_strength
                wt = np.where(np.absolute(wt)>denoise_threshold, wt, 0)

        return self.ifwt(wt,scale=sc,return_length=l)


    def _fourier_denoise(self,input_values, denoise_mode='value',denoise_strength=0.5):
        """
        Perform a Fast Discrete Fourier Transform on the input data, selectively removing frequency components by setting their amplitudes to zero, then reconstruct the original dataset by performing an inverse Fourier transform on the remaining amplitudes.
        

        Parameters
        ============
        input_values : array_like
            The data to be denoised via Walsh transform.


        denoise_mode : {'range', 'value'}, Optional
            The type of filtering to use.
             - **range** will remove a proportion of the higher frequency components based on the denoise_strength value.
             - **value** will remove the frequency components that are below the value based on the denoise_strength.


        denoise_strength : float, Optional
            The strength of the denoising, this parameter controls how the components are altered in order to denoise the input_data.


        Returns
        =============
        array
            denoised data

        """

        l = len(input_values)

        _,ft = self.fft(input_values)

        if denoise_strength >= 0 and denoise_strength < 1:
            if denoise_mode == 'range':
                    filter_idx = int(denoise_strength*len(ft))
                    ft[-filter_idx:] = 0
            else:
                denoise_threshold = np.amax(np.absolute(ft))*denoise_strength
                ft = np.where(np.absolute(ft)>denoise_threshold, ft, 0)

        return self.ifft(ft)


    def sequency_spectrum(self, input_values,pad_mode='constant',**kargs):
        """
        A convenient Sequency power spectrum representation of the input_values data, this will be normalised by the sum of squares of all amplitude values, thus representing a proportional power spectrum.

        Parameters
        ===========
        input_values : array_like
            The data (best to use step change values) to be analysed to generate a sequency power spectrum.

        pad_mode : {None, 'edge','constant'}, Optional
            This is how the input data is to be padded to match the requirement of each Walsh basis being a length which is a power of 2.

            .. note::
                The allowable parameters are the same as those for the Numpy.pad function and therefore any valid mode string or function
                can be used here and it will be passed to the Numpy.pad function.
                
        kargs : any
            Key-value arguments that will be passed to the Numpy.pad function, please see the Numpy.pad documentation for further details of
            allowable kargs for this function.

        Returns
        =============
        tuple(array, array, int)
            sequencies, spectrum_amplitudes, walsh function range

        """

        sf,wm,sc = self.fwt(input_values,pad_mode=pad_mode,**kargs)
        return sf, np.power(wm,2)/(np.sum(np.power(wm,2))),sc


    def frequency_spectrum(self,data,sampling_frequency=1):
        """
        A basic implementation of the Fast Fourier Transform power spectrum as implemented in Numpy.fft.fft.

        Parameters
        =============
        data : array_like
            The data that the frequency spectrum is generated from.

        sampling_frequency : int, Optional
            The sampling frequency used to scale the frequency spectrum, specifically this will need to be tuned based on your data as different scalings will be required to suit the type and density of data points.

        Returns
        ===========
        tuple(array, array)
            frequencies, spectrum_amplitudes

        See Also
        ===========
        Sequency.sequency_spectrum

        References
        =================
        .. https://numpy.org/doc/stable/reference/routines.fft.html

        """

        fourierTransform = np.fft.fft(data)/len(data)
        fourierTransform = fourierTransform[range(int(len(data)/2))]

        tpCount=len(data)
        values=np.arange(int(tpCount/2))
        timePeriod=tpCount/sampling_frequency
        frequencies=values/timePeriod

        return frequencies, np.absolute(fourierTransform)/(np.sum(np.absolute(fourierTransform)))


    def fft(self,data,sampling_frequency=1):
        """
        A basic implementation of the Fast Fourier Transform as implemented in Numpy.fft.fft.

        Parameters
        =============
        data : array_like
            The data that is to be transformed using the fft method from Numpy.

        sampling_frequency : int, Optional
            The sampling frequency used to scale the frequency spectrum, specifically this will need to be tuned based on your data as different scalings will be required to suit the type and density of data points.

        Returns
        ===========
        tuple(array, array)
            frequencies, transform_amplitudes

        See Also
        ===========
        Sequency.sequency_spectrum

        References
        =================
        .. https://numpy.org/doc/stable/reference/routines.fft.html

        """

        fourierTransform = np.fft.fft(data)
        #fourierTransform = fourierTransform[range(int(len(data)/2))]

        tpCount=len(data)
        values=np.arange(int(tpCount/2))
        timePeriod=tpCount/sampling_frequency
        frequencies=values/timePeriod

        return frequencies, fourierTransform


    def ifft(self,data):
        """
        A basic implementation of the inverse Fast Fourier Transform as implemented in Numpy.fft.ifft.

        Parameters
        =============
        data : array_like
            The Fourier transform data that is to be inverted back into the time domain.

        Returns
        ===========
        array
            data

        See Also
        ===========
        Sequency.ifwt

        References
        =================
        .. https://numpy.org/doc/stable/reference/routines.ifft.html

        """

        ifourierTransform = np.fft.ifft(data)

        return ifourierTransform
