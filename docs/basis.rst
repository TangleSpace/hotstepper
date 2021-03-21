=================
Basis and Bases
=================

Basis
=========

    This class represents a wrapper for the function to be used as the representation basis of the steps functions.
    The mathemtical base functions are contained in the Bases static abstract class and are directly referenced from the Basis class.
    All Basis assignments will only reference a Base function to improve performance and Numba compatibility.
    
    **Parameters**
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


    **Methods**
    base : Returns a reference to the assigned base function that is directly callable for evaluation.


Bases
=========

    A static abstract class that holds the definitions for the step and smoothing function bases.

    This class is always referenced statically and therefore serves as a convenience for attaching specific base functions to the basis class.

    These methods are all Numba compiled and therefore best to be seperately out from any direct class inheritence due to performance and possible
    conflicts when copying objects with a referenced Numba function.

    The smoothing bases rely on a limit based definition of the Heaviside function. For example, the ArcTan base is related to the Heaviside base via the following limit of the smoothing parameter.
        
    .. math::
        :nowrap:

        \begin{equation*}
        \theta(t) = \lim_{\alpha \to 0} \left(
        \frac{1}{2}+\frac{1}{\pi}tan^{-1}\left(\frac{t}{\alpha} \right)
            \right)
            \;\;\;\;\; where \;t \in \mathbb{R}
            \end{equation*}

    Using this definition, the limit was set as a function parameter and controls the level of smoothing or alignment to the Heaviside function. All bases methods defined within the HotStepper library are one parameter functions.
        .. note::
            If creating a custom base function, the function must only accept one parameter to control the smoothing and ofcourse the raw steps data for evaluation.


    The mathematical bases defined within this class are:

     - Heaviside
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
     
     - Logistic
        .. math::
            :nowrap:

            \begin{equation*}
            \gamma(t,\alpha) =
            \frac{1}{2} \left(1+tanh\left(\frac{t}{\alpha} \right)
                \right)
                \;\;\;\;\; where \;t,\; \alpha \in \mathbb{R}
                \end{equation*}
     
     - Sigmoid
        .. math::
            :nowrap:

            \begin{equation*}
            \gamma(t,\alpha) =\frac{1}{1+exp\left(-\frac{t}{\alpha} \right)}
            \;\;\;\;\; where \;t,\; \alpha \in \mathbb{R}
            \end{equation*}

     - Arctan
        .. math::
            :nowrap:

            \begin{equation*}
            \gamma(t,\alpha) =
            \frac{1}{2}+\frac{1}{\pi}tan^{-1}\left(\frac{t}{\alpha} \right)
                \;\;\;\;\; where \;t,\; \alpha \in \mathbb{R}
            \end{equation*}

     - Exponential
        .. math::
            :nowrap:

            \begin{equation*}
            \gamma(t,\alpha) =exp\left(-exp\left(-\frac{t}{\alpha} \right)\right)
            \;\;\;\;\; where \;t,\; \alpha \in \mathbb{R}
            \end{equation*}

     - Normal
        .. math::
            :nowrap:

            \begin{equation*}
            \gamma(t,\alpha) =exp\left(-\frac{t^2}{\alpha} \right)
            \;\;\;\;\; where \;t,\; \alpha \in \mathbb{R}
            \end{equation*}

     - Sinc
        .. math::
            :nowrap:

            \begin{equation*}
            \gamma(t,\alpha) =\frac{sin\left(\frac{t}{\alpha} \right)}{\left(t \right)}
            \;\;\;\;\; where \;t,\; \alpha \in \mathbb{R}
            \end{equation*}
