from ..Constants import Constants

class ErrorCode:
    def __init__(self, errorName, errorId, errorType, errorModule, errorDisplaysMsg, errorDisplayMsg):
        setattr(self, Constants.ErrorNameProperty, errorName)
        setattr(self, Constants.ErrorIdProperty, int(errorId))
        setattr(self, Constants.ErrorModuleProperty, errorModule)
        setattr(self, Constants.ErrorTypeProperty, errorType)
        setattr(self, Constants.ErrorDisplaysMsgProperty, errorDisplaysMsg)
        setattr(self, Constants.ErrorDisplayMsgProperty, errorDisplayMsg)