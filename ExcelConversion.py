import xlrd 

from lib.Excel import Constants
from lib.Excel import Column
from lib.ErrorCodes import ErrorCode

from lib.Output import Out

def ExcelSheetErrorCodeListing(fileName, output):
    # To open Workbook 
    with xlrd.open_workbook(fileName) as book:
        sheet = book.sheet_by_index(Constants.ErrorSheet) 
    
        allErrorCodes = []
    
        totalErrorCodes = 0
        
        colPositions = Column.DefineKnownColumnLocations(sheet, output)
        
        for i in range(1, sheet.nrows):
            errorCodeName = sheet.cell_value(i, colPositions[0])
            errorCodeId = sheet.cell_value(i, colPositions[1])
            errorCodeType = sheet.cell_value(i, colPositions[2])
            errorCodeDisplaysMsg = sheet.cell_value(i, colPositions[3])
            errorCodeDisplayMsg = sheet.cell_value(i, colPositions[4])
            if(errorCodeName != '' and errorCodeName[0] != '/'):
                if(errorCodeName[len(errorCodeName)-1] == ',') :
                    errorCodeName = errorCodeName[0:len(errorCodeName)-1]
                totalErrorCodes = totalErrorCodes + 1
                errorCode = ErrorCode.ErrorCode(errorCodeName, errorCodeId, '<Module?>', errorCodeType, errorCodeDisplaysMsg, errorCodeDisplayMsg)
                allErrorCodes.append(errorCode)
        
        output.Verbose(Out.VerbosityLow, 'Total Error Code Count: {} from {}'.format(len(allErrorCodes), fileName))
        
        return allErrorCodes