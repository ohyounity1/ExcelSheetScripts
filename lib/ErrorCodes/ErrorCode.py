from enum import IntEnum
from collections import namedtuple
from dataclasses import dataclass

from ..Constants import Constants
from ..Constants import TableSelections

#ErrorCode = namedtuple('ErrorCode', TableSelections.TableSelections.Values())

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

@dataclass
class ErrorCode:
    ErrorName: str
    ErrorId: int
    ErrorModule: str
    ErrorType: ErrorType
    ErrorDisplaysMsg: bool
    ErrorDisplayMsg: str
    def __str__(self):
        return f'{self.ErrorName}: Id is {self.ErrorId}, Is for module {self.ErrorModule}, is of type {str(self.ErrorType)}, and it displays msg {self.ErrorDisplaysMsg}? of {self.ErrorDisplayMsg}'
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        if isinstance(other, ErrorCode):
            return(self.ErrorName == other.ErrorName and self.ErrorId == other.ErrorId and self.ErrorModule == other.ErrorModule and self.ErrorType == other.ErrorType and self.ErrorDisplaysMsg == other.ErrorDisplaysMsg and self.ErrorDisplayMsg == self.ErrorDisplayMsg)
        return NotImplemented
    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented
    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))


