from lib.Utility import Utility
from lib.Constants import Constants

def PrintBorder(largestColumns):
    formatArgs = []
    formatString = ''
    for c in largestColumns:
        formatArgs.append('-' * c)
        formatString += '|{}'
        
    formatString += '|'
    
    print(formatString.format(*formatArgs))
        
def PrintRow(row, largestColumns):
    formatString = ''
    formatList = []
    for i in row:
        formatString += '%c%-{}s'
        formatList.append('|')
        formatList.append(i)
                
    formatString += '%c'
    formatList.append('|')
    
    finalFormat = formatString.format(*largestColumns)
    
    print(finalFormat % tuple(formatList))
    
def ConvertDisplayMsg(name, data):
    if(name == 'ErrorDisplayMsg'):        
        displayMsg = ''
        if(len(data) > 30):
            displayMsg = '{}...'.format(data[0:30])
        elif(len(data) > 0):
            displayMsg = data
        
        return displayMsg
    elif(name == Constants.ErrorDisplaysMsgProperty or name == Constants.ErrorIdProperty):
        return str(data)
    elif(name == Constants.ErrorTypeProperty):
        strValue = str(data)
        return strValue.replace('ErrorType.', '')
    return data

def Action(columnName, errorCode, dataConverter, largestColumns, dataRow, currentColumnCounter):
    currentColumn = currentColumnCounter[0]
    columnData = getattr(errorCode, columnName)
    columnData = dataConverter(columnName, columnData)
    larger = max(len(columnData), len(columnName))
    if(larger > largestColumns[currentColumn]):
        largestColumns[currentColumn] = larger + 1
    dataRow.append(columnData)
    currentColumnCounter[0] = currentColumn + 1
        
def ErrorListToTableDisplay(errorList, selections):
    tabularFormat = [ ]
    largestColumns = []
    headers = []
    
    # Only include the headers needed
    for header in selections:
        headers.append(header)
        largestColumns.append(0)
    
    for ec in errorList:
        currentColumn = 0
        dataRow = []
        
        currentColumnCounter = [currentColumn]
        
        for header in headers:
            Action(header, ec, ConvertDisplayMsg, largestColumns, dataRow, currentColumnCounter)

        tabularFormat.append(dataRow)

    PrintBorder(largestColumns)
    PrintRow(headers, largestColumns)
    PrintBorder(largestColumns)
    for row in tabularFormat:
        PrintRow(row, largestColumns)
        
    PrintBorder(largestColumns)