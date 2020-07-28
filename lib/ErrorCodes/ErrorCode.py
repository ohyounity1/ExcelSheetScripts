class ErrorCode:
    def __init__(self, errorName, errorId, errorType, errorDisplaysMsg, errorDisplayMsg):
        self.ErrorName = errorName
        self.ErrorId = int(errorId)
        self.ErrorType = errorType
        if(errorDisplaysMsg == 'Y'):
            self.ErrorDisplaysMsg = True
        else:
            self.ErrorDisplaysMsg = False
        self.ErrorDisplayMsg = errorDisplayMsg