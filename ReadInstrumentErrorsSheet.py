def ExcelSheetErrorCodeListing(fileName):
    import xlrd 

    from lib.Excel import Constants
    from lib.Excel import Column
    from lib.ErrorCodes import ErrorCode
    
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
                errorCode = ErrorCode.ErrorCode(errorCodeName, errorCodeId, errorCodeType, errorCodeDisplaysMsg, errorCodeDisplayMsg)
                allErrorCodes.append(errorCode)
        
        output.Verbose(Out.VerbosityLow, 'Total Error Code Count: {} from {}'.format(len(allErrorCodes), fileName))
        
        return allErrorCodes

import sys
import argparse

from lib.Output import Out

output = Out.Out()

parser = argparse.ArgumentParser(description='Retrieve data from Instrument Error Codes Spreadsheets!')
parser.add_argument('-s', '--source', dest='Source', help='Source file name', nargs='+', required=True)
parser.add_argument('-v', '--verbose', dest='Verbosity', help='Verbosity level', action='count', default=0)

#parser.add_argument('-d', '--destination', help'Destination file name', required=True)

arguments = parser.parse_args()

if(len(arguments.Source) > 2):
    output.Error('Too many source arguments!  Only 2 are allowed...')
    
if(len(arguments.Source) > 1 and arguments.Source[0] == arguments.Source[1]):
    output.Error('Error!  Source files are the same name! {}'.format(arguments.Source[0]))

output.Verbosity = arguments.Verbosity
output.Verbose(Out.VerbosityMedium, 'Input files {0}'.format(arguments.Source))

from pathlib import Path

errorCodeListing1 = None
errorCodeListing2 = None

if(Path(arguments.Source[0]).suffix == '.xls' or Path(arguments.Source[0]).suffix == '.xlsx'):
    errorCodeListing1 = ExcelSheetErrorCodeListing(arguments.Source[0])