import enum

#a tracking class for our numpy data model
class DataModel(enum.Enum):
    """
    An enum class that defines the numpy array data model for the step data used throughout the HotStepper library.
    
    """
    
    START = 0
    DIRECTION = 1
    WEIGHT = 2
    VALUE = 3