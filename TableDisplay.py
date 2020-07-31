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
        
        for header in headers:
            DetermineTableStatistics(header, o, __Inner__, largestColumns, dataRow, currentColumnCounter)

        tabularFormat.append(dataRow)

    PrintBorder(largestColumns)
    PrintRow(headers, largestColumns)
    PrintBorder(largestColumns)
    for row in tabularFormat:
        PrintRow(row, largestColumns)
        
    PrintBorder(largestColumns)