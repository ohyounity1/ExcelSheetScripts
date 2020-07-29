from lib.Utility import Utility

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
    elif(name == 'ErrorDisplaysMsg' or name == 'ErrorId'):
        return str(data)
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
        
def TableDisplay(errorList, selections):
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

#        if('ErrorName' in headers):
#            larger = max(len(ec.ErrorName), len(headers[currentColumn]))
#            if(larger > largestColumns[currentColumn]):
#                largestColumns[currentColumn] = larger + 1
#            currentColumn += 1
#            dataRow.append(ec.ErrorName)
#            
#        if('ErrorId' in headers):
#            larger = max(len(str(ec.ErrorId)), len(headers[currentColumn]))
#            if(larger > largestColumns[currentColumn]):
#                largestColumns[currentColumn] = larger + 1
#            currentColumn += 1
#            dataRow.append(ec.ErrorId)
#        
#        if('ErrorModule' in headers):
#            larger = max(len(str(ec.ErrorModule)), len(headers[currentColumn]))
#            if(larger > largestColumns[currentColumn]):
#                largestColumns[currentColumn] = larger + 1
#            currentColumn += 1
#            dataRow.append(ec.ErrorModule)
#            
#        if('ErrorType' in headers):
#            larger = max(len(ec.ErrorType), len(headers[currentColumn]))
#            if(larger > largestColumns[currentColumn]):
#                largestColumns[currentColumn] = larger + 1
#            currentColumn += 1
#            dataRow.append(ec.ErrorType)
#            
#        if('ErrorDisplaysMsg' in headers):
#            larger = max(len(str(ec.ErrorDisplaysMsg)), len(headers[currentColumn]))
#            if(larger > largestColumns[currentColumn]):
#                largestColumns[currentColumn] = larger + 1
#            currentColumn += 1
#            dataRow.append(ec.ErrorDisplaysMsg)
#            
#        if('ErrorDisplayMsg' in headers):
#            displayMsg = ''
#            if(len(ec.ErrorDisplayMsg) > 30):
#                displayMsg = '{}...'.format(ec.ErrorDisplayMsg[0:30])
#            elif(len(ec.ErrorDisplayMsg) > 0):
#                displayMsg = ec.ErrorDisplayMsg
#            larger = max(len(displayMsg), len(headers[currentColumn]))
#            if(larger > largestColumns[currentColumn]):
#                largestColumns[currentColumn] = larger + 1
#            dataRow.append(displayMsg)
            
        tabularFormat.append(dataRow)

    PrintBorder(largestColumns)
    PrintRow(headers, largestColumns)
    PrintBorder(largestColumns)
    for row in tabularFormat:
        PrintRow(row, largestColumns)
        
    PrintBorder(largestColumns)