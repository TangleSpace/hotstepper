from hotstepper.core.Steps import Steps


class Step(Steps):
    """
    This is a wrapper class to make life seem alittle easier if only a single step function is needed and using the plural Steps seems odd.

    Parameters
    -----------    
    start : int, float, datetime_like, Optional
        A quick convenience parameter if this Steps object consists of 1 or 2 steps, the start key can be passed directly in the constructor.
    

    end : int, float, datetime_like, Optional
        A quick convenience parameter if this Steps object consists of 1 or 2 steps, the end key can be passed directly in the constructor.

    weight : int, float, Optional
        A quick convenience parameter if this Steps object consists of 1 or 2 steps, the weight is the step value.

    basis : Basis, Optional
        The is the basis function that will be used for all steps associated with this step function. The default basis -> Basis() is the Heaviside function

    .. math::
        \theta(t) = \left\{
                \begin{array}{ll}
                    0 & \quad t < 0 \
                    1 & \quad t \geq 0
                \end{array}
            \right.
        where $t \in \mathbb{R}
        
    """
    
    def __init__(self, start=None, end = None, weight = None, use_datetime = False, basis = None):
        super().__init__(start=start, end=end, weight=weight, use_datetime=use_datetime,basis=basis)