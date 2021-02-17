import numpy as np
from hotstepper.core.data_model import DataModel
from hotstepper.utilities.helpers import get_epoch_start


def apply_math_function(caller,other,math_function, sample_points=None):
    """
    Apply the supplied function to two objects evaluated at the union of all their unique step keys.

    For example, math_function = numpy.multiply will multiple the step values from each steps object together at each of the step keys that forms the union set of all step keys.
    Simply, a list of unique step keys will be generated based on those from each steps object and the provided function will be applied across all steps values at each of those keys to generate a new steps object.

    If the second argument is a scalar, this value will be broadcast to match the number of step keys in the longest step or steps object.

    Parameters
    ===========
    caller : Step, Steps
        The parent object with step values to perform the math operation on

    other : int, float, Step, Steps
        Steps or scalar value to be combined with the caller object values evaluated at the common union of step keys using the provided math_function.

    math_function : math_like function, e.g. numpy.add, operator.__mul__
        A binary math function that accepts two arguments and returns an array the same length as the longest input, e.g +,-,*,/, np.add, np.multiply etc.

    sample_points : array_like of int,float or datetime_like, Optional
        Specifiy the specific points the math_function function is to be evaluated across all provided step functions.

    Returns
    ==========
    Steps
        A new steps object containing the result of the function application across the provided objects.

    See Also
    ============
    filter_values
    apply_reduction_function

    Examples
    ==========

    """

    return _apply_aggreduce_function(
            steps_to_combine=[caller,other],
            agg_reduce_function=math_function,
            sample_points=sample_points,
            is_agg_function=True
        )


def apply_reduction_function(steps_to_combine,reduction_function,sample_points=None):
    """
    Apply the supplied function to all provided objects evaluated at the union of all their unique step keys.

    For example, reduction_function = numpy.mean will find the mean across all objects evaluated at each step key that is from the union set of all keys.
    Simply, a list of unique step keys will be generated based on those from each steps object and the provided function will be applied across all steps values at each of those keys to generate a new steps object.

    If the second argument is a scalar, this value will be broadcast to match the number of step keys in the longest step or steps object.

    Parameters
    ===========
    steps_to_combine : int, float, Step, Steps
        Objects and/or numbers to apply the reduction function at each of the unique keys.

    reduction_function : math_like function
        A reduction function that returns a scalar for each input array, e.g mean, variance, np.mean, np.std, np.median etc.

    sample_points: array_like of int,float or datetime_like, Optional
        Specifiy the specific points the reduction_function function is to be evaluated across all provided step functions.

    Returns
    ==========
    Steps
        A new steps object containing the result of the function application across the provided objects.

    See Also
    ============
    filter_values
    apply_math_function

    Examples
    ==========

    """

    return _apply_aggreduce_function(
                steps_to_combine=steps_to_combine,
                agg_reduce_function=reduction_function,
                sample_points=sample_points,
                is_agg_function=False
            )


def _apply_aggreduce_function(steps_to_combine,agg_reduce_function,sample_points=None, is_agg_function=True):
    """
    Apply the supplied function to all provided objects evaluated at the union of their unique step keys.

    For example, aggregation_function = numpy.mean will find the mean across all objects evaluated at each step key that is from the union set of all keys from each steps function.
    Simply, a list of unique step keys will be generated based on those from each steps object and the provided function will be applied across all steps values at each of those keys to generate a new steps object.

    If the second argument is a scalar, this value will be broadcast to match the number of step keys in the longest step or steps object.

    Parameters
    ===========
    steps_to_combine : int, float, Step, Steps
        Any value to compare each step component against.

    agg_reduce_function : math_like function, e.g. aggreation functions like numpy.add, operator.__mul__ or reduction functions like mean, std etc.
        A reduction function that returns a scalar for each input array, e.g mean, variance, np.mean, np.std, np.median etc.

    sample_points : array_like of int,float or datetime_like, Optional
        Specifiy the specific points the agg_reduce_function function is to be evaluated across all provided step functions.

    is_agg_function : bool, Optional
        Flag to indicate if the is_agg_function is either an aggregation type such as the mathematical operations +,-,/,* or a reduction type such as mean, max, median.

    Returns
    ==========
    Steps
        A new steps object containing the result of the function application across the provided objects.

    See Also
    ============
    filter_values
    apply_reduction_function
    apply_math_function

    Examples
    ==========

    """
 
    #used to check if objects are implementing the AbstractSteps interface
    ty = type(steps_to_combine[0])
    base_parent = ty.__base__

    if sample_points is None:
        keys = np.sort(np.unique(np.concatenate([s.step_keys() for s in steps_to_combine if isinstance(s,base_parent)])))
    else:
        keys = sample_points

    #to handle int float as well as AbstractSteps in one go
    get_stack_value = lambda x: x.step(keys,False) if isinstance(x,base_parent) else np.full(len(keys),x)
    stack = np.array([get_stack_value(s) for s in steps_to_combine])

    if is_agg_function:
        result = np.diff(agg_reduce_function(*stack),prepend=0)
    else:
        result = np.diff(agg_reduce_function(stack,axis=0),prepend=0)
    
    step_data = np.empty((keys.shape[0],3))
    step_data[:,DataModel.START.value] = keys
    step_data[:,DataModel.DIRECTION.value] = 1
    step_data[:,DataModel.WEIGHT.value] = result

    #filter out values that create issues
    step_data = step_data[~np.isnan(step_data[:,DataModel.WEIGHT.value])]
    step_data = step_data[step_data[:,DataModel.WEIGHT.value]!=0]
    step_data = step_data[step_data[:,DataModel.WEIGHT.value]!=np.PINF]
    step_data = step_data[step_data[:,DataModel.WEIGHT.value]!=np.NINF]
    
    #promote the Steps key type if any of the steps to combine are using datetime
    any_using_datetime = (np.array([s.using_datetime() for s in steps_to_combine if isinstance(s,base_parent)])==True).any()

    ty = type(steps_to_combine[0])
    result_step = ty(use_datetime=any_using_datetime,basis=steps_to_combine[0].basis())

    if step_data.shape[0] > 0:
        return result_step.add_steps(step_data)
    else:
        return result_step


def filter_values(caller,other, operation_func, normalise_value = 0):
    """
    This function is used to create a filtered version of the steps by removing steps not evaluating to true from applying the comparison function at all step change locations.

    Parameters
    ===========
    other : int, float
        Any value to compare each steps value against.

    operation_func : binary boolean function
        A binary comparison function that returns a bool, e.g >,<,==.

    normalise_value: int, float, Optional
        A value to assign at the step keys that are included in the return object. If a value of zero is used, the return object will have the value of the step function between the included step keys.

    Returns
    ==========
    Steps
        A new steps object containing the result of the function application across the provided objects.

    See Also
    ============
    apply_reduction_function
    apply_math_function

    """

    if type(other) in [float,int]:

        caller_step_data = caller.steps()
        mask = np.where(operation_func(caller_step_data[:,DataModel.WEIGHT.value],other), True,False)

        if np.alltrue(mask):
            if normalise_value == 0:
                return caller
            else:
                ty = type(caller)
                return ty(use_datetime=caller.using_datetime(),
                            basis=caller.basis(),
                            start=caller.first(),
                            end=caller.last(),
                            weight=normalise_value
                        )

        new_steps = _filter_by_mask(caller_step_data,mask,normalise_value)
    else:
        caller_step_data = caller.steps()
        other_step_values = other(caller.step_keys())

        mask = np.where(operation_func(caller_step_data[:,DataModel.WEIGHT.value],other_step_values), True,False)

        if np.alltrue(mask):
            if normalise_value == 0:
                return caller
            else:
                ty = type(caller)
                return ty(use_datetime=caller.using_datetime(),
                            basis=caller.basis(),
                            start=caller.first(),
                            end=caller.last(),
                            weight=normalise_value
                        )
        
        new_steps = _filter_by_mask(caller_step_data,mask,normalise_value)

    #we have the data, now return an object matching the caller, something that implements the AbstractSteps interface
    ty = type(caller)
    result_step = ty(use_datetime=caller.using_datetime(),basis=caller.basis())

    if len(new_steps) > 0:
        return result_step.add_steps(np.array(new_steps))
    else:
        return result_step


def _filter_by_mask(step_data,mask,normalise_value = 0):

        if np.alltrue(mask):
            return step_data

        new_steps = []

        st = None
        adj = 0
        for i ,s in enumerate(step_data[:,DataModel.START.value]):
            if mask[i]:
                if st is None:
                    st = i
                    if normalise_value == 0:
                        new_steps.append([s,1,step_data[i,DataModel.WEIGHT.value]])
                    else:
                        new_steps.append([s,1,normalise_value])
                elif st is not None and (i > st) and normalise_value == 0:
                    new_steps.append([s,1,step_data[i,DataModel.DIRECTION.value]])
                    adj += step_data[i,DataModel.DIRECTION.value]
            else:
                if st is not None and st != get_epoch_start(False):
                    if normalise_value == 0:
                        new_steps.append([s,1,-1*(step_data[st,DataModel.WEIGHT.value] + adj)])
                        adj = 0
                    else:
                        new_steps.append([s,1,-1*normalise_value])
                    st = None
        
        return new_steps
