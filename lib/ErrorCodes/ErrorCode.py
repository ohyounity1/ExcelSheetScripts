from ..Constants import Constants

class ErrorCode:
    def __init__(self, errorName, errorId, errorModule, errorType, errorDisplaysMsg, errorDisplayMsg):
        setattr(self, Constants.ErrorNameProperty, errorName)
        setattr(self, Constants.ErrorIdProperty, errorId)
        setattr(self, Constants.ErrorModuleProperty, errorModule)
        setattr(self, Constants.ErrorTypeProperty, errorType)
        setattr(self, Constants.ErrorDisplaysMsgProperty, errorDisplaysMsg)
        setattr(self, Constants.ErrorDisplayMsgProperty, errorDisplayMsg)