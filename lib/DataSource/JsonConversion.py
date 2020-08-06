import json

from lib.Constants import Constants
from lib.ErrorCodes import ErrorCode
from lib.Output import Out

from . import RetrieveMethods

@RetrieveMethods.RetrieveAllResults
@RetrieveMethods.RetrieveErrorCodes
def JsonFileErrorCodeListing(fileName, allErrorCodes):
    with open(fileName) as jsonFileContents:
        errorCodesJson = json.load(jsonFileContents)
        errorCodesJsonListing = errorCodesJson['AllErrors']
        
        for errorCodeJson in errorCodesJsonListing:
            errorCodeName = errorCodeJson['ErrorCode']
            errorCodeId = -1
            errorCodeModule = errorCodeJson['Module']
            errorCodeTypeStr = errorCodeJson['ErrorType']

            errorCodeType = ''
            if('ServiceCall' == errorCodeTypeStr):
                errorCodeType = ErrorCode.ErrorType.ServiceCall()
            elif('AssistanceNeeded' == errorCodeTypeStr):
                errorCodeType = ErrorCode.ErrorType.AssistanceNeeded()
            elif('Warning' == errorCodeTypeStr):
                errorCodeType = ErrorCode.ErrorType.Warning()

            errorCodeDisplaysMsg = errorCodeJson['DisplayToUser']
            errorCodeDisplayMsg = errorCodeJson['DisplayMessage']

            Out.VerbosePrint(Out.Verbosity.HIGH, 'Read in JSON Sheet Line: {}, {}, {}'.format(errorCodeName, errorCodeModule, str(errorCodeType)))

            errorCode = ErrorCode.ErrorCode(errorCodeName, errorCodeId, errorCodeModule, errorCodeType, errorCodeDisplaysMsg, errorCodeDisplayMsg)
            allErrorCodes.append(errorCode)
