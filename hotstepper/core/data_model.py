import enum

#a tracking class for our numpy data model
class DataModel(enum.Enum):
    """
    An enum class that defines the numpy array data model for the step data used throughout the HotStepper library. This class represents the layout of the steps data by index.


    **START** : The step key value index within the data structure.

    **DIRECTION** : The step delta direction value index within the data structure.

    **WEIGHT** : The step amount of strength value index within the data structure.

    **VALUE** : The step cummulative value index within the data structure.
    
    """
    
    START = 0
    DIRECTION = 1
    WEIGHT = 2
    VALUE = 3