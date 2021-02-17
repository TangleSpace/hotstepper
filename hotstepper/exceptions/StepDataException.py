class StepDataException(Exception):
    """
    This exception is raised when incorrect or corrupt data is attempted to be loaded into a Steps object.


    Parameters
    ===========
    msg : str
        Human readable string describing the exception.
    code : :obj:`int`, optional
        Numeric error code.

    """

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code


class EmptyStepException(Exception):
    """
    This exception is raised when an operation is called on an empty Steps object.

    Parameters
    ===========
    msg : str
        Human readable string describing the exception.
    code : :obj:`int`, optional
        Numeric error code.

    """

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code