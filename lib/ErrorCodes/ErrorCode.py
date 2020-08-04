from enum import IntEnum
from collections import namedtuple

from ..Constants import Constants
from ..Constants import TableSelections

ErrorCode = namedtuple('ErrorCode', TableSelections.TableSelections.Values())

class ErrorType(IntEnum):
    UNKNOWN = 0
    SERVICE_CALL = 1
    ASSISTANCE_NEEDED = 2
    WARNING = 3
    __Mapping__ = { 
        UNKNOWN: 'Unknown',
        SERVICE_CALL : 'ServiceCall',
        ASSISTANCE_NEEDED : 'AssistanceNeeded',
        WARNING : 'Warning'
    }
    def __init__(self, type):
        self.Type = type
    def __repr__(self):
        return self.__Mapping__[self.Type]
    def __str__(self):
        return self.__repr__()
    def ServiceCall():
        return ErrorType(ErrorType.SERVICE_CALL)
    def AssistanceNeeded():
        return ErrorType(ErrorType.ASSISTANCE_NEEDED)
    def Warning():
        return ErrorType(ErrorType.WARNING)