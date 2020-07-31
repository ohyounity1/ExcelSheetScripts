from enum import IntEnum

from ..Constants import Constants

class ErrorCode:
    def __init__(self, errorName, errorId, errorModule, errorType, errorDisplaysMsg, errorDisplayMsg):
        setattr(self, Constants.ErrorNameProperty, errorName)
        setattr(self, Constants.ErrorIdProperty, errorId)
        setattr(self, Constants.ErrorModuleProperty, errorModule)
        setattr(self, Constants.ErrorTypeProperty, errorType)
        setattr(self, Constants.ErrorDisplaysMsgProperty, errorDisplaysMsg)
        setattr(self, Constants.ErrorDisplayMsgProperty, errorDisplayMsg)


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