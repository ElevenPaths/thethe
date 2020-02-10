from enum import Enum, unique


@unique
class PluginResultStatus(Enum):
    STARTED = (0,)
    COMPLETED = (1,)
    RETURN_NONE = (2,)
    FAILED = (3,)
    NO_API_KEY = 4
