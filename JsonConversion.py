import json

from lib.Constants import Constants
from lib.ErrorCodes import ErrorCode
from lib.Output import Out
from lib.Constants import ErrorTypes

def JsonFileErrorCodeListing(fileName, output):
    with open(fileName) as jsonFileContents:
        errorCodesJson = json.load(jsonFileContents)
        errorCodesJsonListing = errorCodesJson['AllErrors']
        
        allErrorCodes = []
    
        totalErrorCodes = 0
        
        for errorCodeJson in errorCodesJsonListing:
            errorCodeName = errorCodeJson['ErrorCode']
            errorCodeId = -1
            errorCodeModule = errorCodeJson['Module']
            errorCodeType = errorCodeJson['ErrorType']
            errorCodeDisplaysMsg = errorCodeJson['DisplayToUser']
            errorCodeDisplayMsg = errorCodeJson['DisplayMessage']
            errorCode = ErrorCode.ErrorCode(errorCodeName, errorCodeId, errorCodeModule, errorCodeType, errorCodeDisplaysMsg, errorCodeDisplayMsg)
            allErrorCodes.append(errorCode)
            totalErrorCodes = totalErrorCodes + 1
            
        output.Verbose(Out.VerbosityLow, 'Total Error Code Count: {} from {}'.format(len(allErrorCodes), fileName))
        
        return allErrorCodes