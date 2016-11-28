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
    ORIGINAL_LOOPING='/no_changes/looping'
    ORIGINAL_NOT_LOOPING='/no_changes/not_looping'
    INITIAL_RESULTS='/initial_results'
    MULTIPLE_MUTEXES='/optimization_case_studies/multiple_mutexes'
    LOCK_FREE='/optimization_case_studies/lock_free'
    COPIES='/observation_studies/copying_data'
    NO_COPIES='/observation_studies/copying_data/no_cpd_object'
    TASKS='/observation_studies/task_scheduling'
    GAME_LOGIC_TASKS='/observation_studies/task_scheduling/game_logic_tasks'
    NOT_THREADED='/observation_studies/task_scheduling/not_threaded'
    FAILURE='/observation_studes/emission_failure'
    FAILURE_SOLUTION='/observation_studies/emission_failure/solution'
