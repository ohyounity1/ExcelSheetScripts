
def TableDisplay(errorList, selections):
    tabularFormat = [ ]
    largestColumns = []
    headers = []
    
    # Only include the headers needed
    desiredHeaders = [value for value in vars(errorList[0]) if value in selections] 
    for header in desiredHeaders:
        headers.append(header)
        largestColumns.append(0)
    
    for ec in errorList:
        currentColumn = 0
        dataRow = []
        
        if('ErrorName' in headers):
            larger = max(len(ec.ErrorName), len(headers[currentColumn]))
            if(larger > largestColumns[currentColumn]):
                largestColumns[currentColumn] = larger + 1
            currentColumn += 1
            dataRow.append(ec.ErrorName)
            
        if('ErrorId' in headers):
            larger = max(len(str(ec.ErrorId)), len(headers[currentColumn]))
            if(larger > largestColumns[currentColumn]):
                largestColumns[currentColumn] = larger + 1
            currentColumn += 1
            dataRow.append(ec.ErrorId)
        
        if('ErrorModule' in headers):
            larger = max(len(str(ec.ErrorModule)), len(headers[currentColumn]))
            if(larger > largestColumns[currentColumn]):
                largestColumns[currentColumn] = larger + 1
            currentColumn += 1
            dataRow.append(ec.ErrorModule)
            
        if('ErrorType' in headers):
            larger = max(len(ec.ErrorType), len(headers[currentColumn]))
            if(larger > largestColumns[currentColumn]):
                largestColumns[currentColumn] = larger + 1
            currentColumn += 1
            dataRow.append(ec.ErrorType)
            
        if('ErrorDisplaysMsg' in headers):
            larger = max(len(str(ec.ErrorDisplaysMsg)), len(headers[currentColumn]))
            if(larger > largestColumns[currentColumn]):
                largestColumns[currentColumn] = larger + 1
            currentColumn += 1
            dataRow.append(ec.ErrorDisplaysMsg)
            
        if('ErrorDisplayMsg' in headers):
            displayMsg = ''
            if(len(ec.ErrorDisplayMsg) > 30):
                displayMsg = '{}...'.format(ec.ErrorDisplayMsg[0:30])
            elif(len(ec.ErrorDisplayMsg) > 0):
                displayMsg = ec.ErrorDisplayMsg
            larger = max(len(displayMsg), len(headers[currentColumn]))
            if(larger > largestColumns[currentColumn]):
                largestColumns[currentColumn] = larger + 1
            dataRow.append(displayMsg)
            
        tabularFormat.append(dataRow)

    PrintBorder(largestColumns)
    PrintRow(headers, largestColumns)
    PrintBorder(largestColumns)
    for row in tabularFormat:
        PrintRow(row, largestColumns)
        
    PrintBorder(largestColumns)

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

    #if(len(row) == 1 and len(largestColumns) == 1):
    #    print('%c%-{}s%c'.format(largestColumns[0]) % ('|', headers[0], '|'))
    #if(len(row) == 2 and len(largestColumns) == 2):
    #    print('%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1]) % ('|', headers[0], '|', headers[1], '|'))
    #if(len(row) == 3 and len(largestColumns) == 3):
    #    print('%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2]) % ('|', headers[0], '|', headers[1], '|', headers[2], '|'))
    #if(len(row) == 3 and len(largestColumns) == 3):
    #    print('%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2]) % ('|', headers[0], '|', headers[1], '|', headers[2], '|'))
    #if(len(row) == 5):
    #    print('%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2], largestColumns[3], largestColumns[4]) % ('|', headers[0], '|', headers[1], '|', headers[2], '|', headers[3], '|', headers[4], '|'))
    #print('|{}|{}|{}|{}|{}|'.format('-' * (largestColumns[0]), '-' * (largestColumns[1]),  '-' * (largestColumns[2]),  '-' * (largestColumns[3]),  '-' * (largestColumns[4])))
    #print('%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2], largestColumns[3], largestColumns[4]) % ('|', headers[0], '|', headers[1], '|', headers[2], '|', headers[3], '|', headers[4], '|'))
    #print('|{}|{}|{}|{}|{}|'.format('-' * (largestColumns[0]), '-' * (largestColumns[1]), '-' * (largestColumns[2]), '-' * (largestColumns[3]), '-' * (largestColumns[4])))
    #for ec in tabularFormat:
    #    print('%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2], largestColumns[3], largestColumns[4]) % ('|', ec[0], '|', ec[1], '|', ec[2], '|', ec[3], '|', ec[4], '|'))
    #print('|{}|{}|{}|{}|{}|'.format('-' * (largestColumns[0]), '-' * (largestColumns[1]), '-' * (largestColumns[2]), '-' * (largestColumns[3]), '-' * (largestColumns[4])))
    
    
if __name__ == "__main__":
    PrintRow(['hi'], [5])