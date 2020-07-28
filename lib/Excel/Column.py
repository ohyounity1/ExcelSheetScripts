ErrorCodeNameHeader = 'FW Error Enum'
ErrorCodeIdHeader = 'Error Code'
ErrorCodeTypeHeader = 'Error Type'
ErrorCodeDisplaysMsgHeader = 'SW User Message'
ErrorCodeDisplayMsgHeader = 'User message'

from . import Constants
from ..Output import Out
def DefineKnownColumnLocations(sheet, output):
    errorNameCol = None
    errorIdCol = None
    errorTypeCol = None
    errorDisplaysMsgCol = None
    errorDisplayMsgCol = None
    
    for column in range(0, sheet.ncols):
        cellHeader = sheet.cell_value(Constants.HeaderRow, column)
        output.Verbose(Out.VerbosityHigh, 'Column Name: {0}'.format(cellHeader))
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
        output.Error('Did not find all columns!')
        
    return (errorNameCol, errorIdCol, errorTypeCol, errorDisplaysMsgCol, errorDisplayMsgCol)