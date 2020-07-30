from enum import Enum

class ErrorType(Enum):
    UNKNOWN = None
    SERVICE_CALL = 0
    ASSISTANCE_NEEDED = 1
    WARNING = 2