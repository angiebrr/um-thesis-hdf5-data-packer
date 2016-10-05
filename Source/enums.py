from enum import Enum, unique

@unique
class ColTypeEnum(Enum):
    """ The different types of column types that can be inferred from a CSV
    """
    UNKNOWN = 1
    STRING = 2
    FLOAT = 3
    INT = 4

@unique
class OSEnum(Enum):
    """The different OSes that will generate the csv data
    """
    WINDOWS='windows'
    IOS='ios'
    ANDROID='android'

@unique 
class DataGroupEnum(Enum):
    """The groups that will be used which depends on the experiment done
    """
    MULTIPLE_MUTEXES='/optimizations/multiple_mutexes'
    LOCK_FREE='/optimizations/lock_free'
    USELESS_OPTIMIZATIONS='/case_studies/useless_optimizations'
    FAILING_EMISSIONS='/case_studies/failing_emissions'
    TASK_TYPES='/case_studies/task_types'
    OBJECT_CONTENTION='/case_studies/object_contention'
