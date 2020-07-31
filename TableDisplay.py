from lib.Utility import Utility
from lib.Constants import Constants

from lib.Output import Out

def PrintBorder(largestColumns):
    formatArgs = []
    formatString = ''
    for c in largestColumns:
        formatArgs.append('-' * c)
        formatString += '|{}'
        
    formatString += '|'
    
    Out.RegularPrint(formatString.format(*formatArgs))
        
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
    
    Out.RegularPrint(finalFormat % tuple(formatList))


def DetermineTableStatistics(columnName, errorCode, dataConverter, largestColumns, dataRow, currentColumnCounter):
    currentColumn = currentColumnCounter[0]
    columnData = getattr(errorCode, columnName)
    columnData = dataConverter(columnName, columnData)
    larger = max(len(columnData), len(columnName))
    if(larger > largestColumns[currentColumn]):
        largestColumns[currentColumn] = larger + 1
    dataRow.append(columnData)
    currentColumnCounter[0] = currentColumn + 1
        
def ErrorListToTableDisplay(objects, headers, msgConverter=None):
    def __Inner__(colName, msg):
        if(msgConverter == None): 
            return msg
        return msgConverter(colName, msg)

    tabularFormat = []
    largestColumns = [0 for _ in headers]
    
    for o in objects:
        currentColumn = 0
        dataRow = []
        
        currentColumnCounter = [currentColumn]
        
        headerCount = 0
        for header in headers:
            DetermineTableStatistics(header, o, __Inner__, largestColumns, dataRow, currentColumnCounter)
            headerCount += 1

        debugOutput = 'Row Data: '
        for i in range(0, headerCount):
            debugOutput += f'{headers[i]} : {dataRow[i]}'

        Out.VerbosePrint(Out.Verbosity.HIGH, f'Tabling the object: {debugOutput}')
        tabularFormat.append(dataRow)

    PrintBorder(largestColumns)
    PrintRow(headers, largestColumns)
    PrintBorder(largestColumns)
    for row in tabularFormat:
        PrintRow(row, largestColumns)
        
    PrintBorder(largestColumns)