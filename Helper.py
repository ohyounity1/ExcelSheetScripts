from lib.Output import Out
from lib.DataSource import DataSources
from lib.Utility import Utility
from lib.Constants import Constants

def RetrieveAllResults(sourceFile):
    Out.VerbosePrint(Out.Verbosity.LOW, 'Source File Name: {0}'.format(sourceFile))

    errorCodes = DataSources.RetrieveErrorCodes(sourceFile)

    if(errorCodes is None or len(errorCodes) == 0):
        Out.ErrorPrint('There were no error codes found in {}!'.format(sourceFile))

    return errorCodes

__DefaultSelection__ = {
    '.xls' : [Constants.ErrorModuleProperty],
    '.xlsx': [Constants.ErrorModuleProperty],
    '.json': [Constants.ErrorIdProperty]
}

def ConvertErrorTypeDisplayMsg(name, data):
    if(name == 'FirstValue' or name == 'SecondValue'):
        return str(data)
    return data

def ConvertDisplayMsg(name, data):
    if(name == Constants.ErrorDisplayMsgProperty):        
        displayMsg = ''
        if(len(data) > Constants.MaxDisplayStringForTable):
            displayMsg = '{}...'.format(data[0:Constants.MaxDisplayStringForTable])
        elif(len(data) > 0):
            displayMsg = data
        return displayMsg
    elif(name == Constants.ErrorDisplaysMsgProperty or name == Constants.ErrorIdProperty):
        return str(data)
    elif(name == Constants.ErrorTypeProperty):
        return str(data)
    return data

def ErrorCodeTableDisplay(sourceFile, errorCodes, destination, selectedColumns):
    import TableDisplay

    selectedOrder = selectedColumns

    # Default to all available columns if nothing given by user
    if(len(selectedOrder) == 0):
        from pathlib import Path
        extension = Path(sourceFile).suffix
        # Read out all the properties available
        selectedOrder = Utility.IntrospectObject(errorCodes[0], [Constants.ErrorNameProperty, 
            Constants.ErrorIdProperty,
            Constants.ErrorModuleProperty,
            Constants.ErrorTypeProperty,
            Constants.ErrorDisplaysMsgProperty,
            Constants.ErrorDisplayMsgProperty], lambda e: e not in __DefaultSelection__[extension])
    
    Out.VerbosePrint(Out.Verbosity.LOW, 'Items selected for display {}'.format(selectedOrder))
    
    if(destination == 'Prompt'):
        # Print all results to output
        Out.RegularPrint('Source Display for {}'.format(sourceFile))
        TableDisplay.ErrorListToTableDisplay(errorCodes, selectedOrder, ConvertDisplayMsg)
    elif(destination == 'CSV'):
        with open('ErrorCodesListing.csv', 'w') as csvFile:

            # Print all results to output
            csvFile.write('Source Display for {}'.format(sourceFile))
            headerString = ''

            for i in range(0, len(selectedOrder)):
                headerString += f'{selectedOrder[i]}'
                if(i < len(selectedOrder) - 1):
                    headerString += ','
            csvFile.write(f'\n{headerString}')

            rowString = ''
            for errorCode in errorCodes:
                rowString = ''
                for i in range(0, len(selectedOrder)):
                    propertyValue = getattr(errorCode,selectedOrder[i])
                    if(selectedOrder[i] == 'ErrorDisplayMsg'):
                        propertyValue = propertyValue.replace('"', '""')
                        rowString += f'"{propertyValue}"'
                    else:
                        rowString += f'{propertyValue}'
                    if(i < len(selectedOrder) - 1):
                        rowString += ','
                csvFile.write(f'\n{rowString}')