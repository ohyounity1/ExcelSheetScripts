from ..Constants import Constants
from ..ErrorCodes import ErrorCode
from ..Output import Out

from . import RetrieveMethods

def __DefineKnownColumnLocations(sheet) -> (str, str, str, str, str):
    errorNameCol = None
    errorIdCol = None
    errorTypeCol = None
    errorDisplaysMsgCol = None
    errorDisplayMsgCol = None
    
    ErrorCodeNameHeader = 'FW Error Enum'
    ErrorCodeIdHeader = 'Error Code'
    ErrorCodeTypeHeader = 'Error Type'
    ErrorCodeDisplaysMsgHeader = 'SW User Message'
    ErrorCodeDisplayMsgHeader = 'User message'

    for column in range(0, sheet.ncols):
        cellHeader = sheet.cell_value(0, column)
        Out.VerbosePrint(Out.Verbosity.HIGH, 'Column Name: {}'.format(cellHeader))
        if(ErrorCodeNameHeader in cellHeader):
            errorNameCol = column
        if(ErrorCodeIdHeader in cellHeader):
            errorIdCol = column
        if(ErrorCodeTypeHeader in cellHeader):
            errorTypeCol = column
        if(ErrorCodeDisplaysMsgHeader in cellHeader):
            errorDisplaysMsgCol = column
        if(ErrorCodeDisplayMsgHeader in cellHeader):
            errorDisplayMsgCol = column
            
    if(errorNameCol is None or
       errorIdCol is None or
       errorTypeCol is None or
       errorDisplaysMsgCol is None or
       errorDisplayMsgCol is None):
        Out.ErrorPrint('Did not find all columns!')
        
    return (errorNameCol, errorIdCol, errorTypeCol, errorDisplaysMsgCol, errorDisplayMsgCol)

@RetrieveMethods.RetrieveAllResults
@RetrieveMethods.RetrieveErrorCodes
def ExcelSheetErrorCodeListing(fileName, allErrorCodes) -> [ErrorCode.ErrorCode]:
    import xlrd 

    def ErrorId(errorIdStr):
        if(isinstance(errorIdStr, float)):
            return int(errorIdStr)
        return errorIdStr
    # To open Workbook 
    with xlrd.open_workbook(fileName) as book:
        sheet = book.sheet_by_index(Constants.ErrorSheet) 
    
        colPositions = __DefineKnownColumnLocations(sheet)
        
        for i in range(1, sheet.nrows):
            errorCodeName = sheet.cell_value(i, colPositions[0]).strip()
            errorCodeId = sheet.cell_value(i, colPositions[1])
            errorCodeTypeStr = sheet.cell_value(i, colPositions[2]).strip()
            
            errorCodeType = ''
            if('Service Call' in errorCodeTypeStr):
                errorCodeType = ErrorCode.ErrorType.ServiceCall()
            elif('Assistance Needed' in errorCodeTypeStr):
                errorCodeType = ErrorCode.ErrorType.AssistanceNeeded()
            elif('Warning' in errorCodeTypeStr):
                errorCodeType = ErrorCode.ErrorType.Warning()
                
            errorCodeDisplaysMsg = (lambda x: x.lower() == 'y' or x.lower() == 'yes')(sheet.cell_value(i, colPositions[3]).strip())
            errorCodeDisplayMsg = sheet.cell_value(i, colPositions[4]).strip()
            
            Out.VerbosePrint(Out.Verbosity.HIGH, 'Read in Excel Sheet Line: {}, {}, {}'.format(errorCodeName, ErrorId(errorCodeId), str(errorCodeType)))
            if(errorCodeName != '' and errorCodeName[0] != '/'):
                if(errorCodeName[len(errorCodeName)-1] == ',') :
                    Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Cleaning up error code {}'.format(errorCodeName))
                    errorCodeName = errorCodeName[0:len(errorCodeName)-1]
                    Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Cleaned up error code {}'.format(errorCodeName))
                errorCode = ErrorCode.ErrorCode(errorCodeName, int(errorCodeId), Constants.UnknownModuleType, errorCodeType, errorCodeDisplaysMsg, errorCodeDisplayMsg)
                allErrorCodes.append(errorCode)