import json

from lib.Constants import Constants
from lib.ErrorCodes import ErrorCode
from lib.Output import Out
from lib.Constants import ErrorTypes

def JsonFileErrorCodeListing(fileName, allErrorCodes):
    with open(fileName) as jsonFileContents:
        errorCodesJson = json.load(jsonFileContents)
        errorCodesJsonListing = errorCodesJson['AllErrors']
        
        for errorCodeJson in errorCodesJsonListing:
            errorCodeName = errorCodeJson['ErrorCode']
            errorCodeId = -1
            errorCodeModule = errorCodeJson['Module']
            errorCodeType = errorCodeJson['ErrorType']
            errorCodeDisplaysMsg = errorCodeJson['DisplayToUser']
            errorCodeDisplayMsg = errorCodeJson['DisplayMessage']
            errorCode = ErrorCode.ErrorCode(errorCodeName, errorCodeId, errorCodeModule, errorCodeType, errorCodeDisplaysMsg, errorCodeDisplayMsg)
            allErrorCodes.append(errorCode)
