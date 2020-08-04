from lib.Output import Out
from lib.DataSource import DataSources
from lib.Utility import Utility
from lib.Constants import Constants
from lib.Constants import Destinations

from lib.Output import TableDisplay
from lib.Output import CsvDisplay

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

class ErrorDisplay:
    def __init__(self, headerPrinter):
        self.HeaderPrinter = headerPrinter
    def DisplayErrors(self, source, errorCodes, selectedOrder, converter):
        self.HeaderPrinter(f'Source Display for {source}')
        self.__DisplayErrors__(errorCodes, selectedOrder, converter)
    def __DisplayErrors__(self, errorCodes, selectedOrder, converter):
        pass

class TableErrorDisplay(ErrorDisplay):
    def __init__(self):
        super().__init__(Out.RegularPrint)
    def __DisplayErrors__(self, errorCodes, selectedOrder, converter):
        TableDisplay.ErrorListToTableDisplay(errorCodes, selectedOrder, converter)

class CsvErrorDisplay(ErrorDisplay):
    def __init__(self, fileName):
        self.File = open(fileName, 'w')
        super().__init__(self.File.write)
    def __DisplayErrors__(self, errorCodes, selectedOrder, converter):
        CsvDisplay.ErrorListToCSVDisplay(self.File, errorCodes, selectedOrder, converter)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.File.close()

def ErrorCodeDisplay(sourceFile, errorCodes, arguments, tableConverterMethod, exportFile, exportConverterMethod):
    def __Wrapper__(display, sourceFile, errorCodes, selectedOrder, converter):
        display.DisplayErrors(sourceFile, errorCodes, selectedOrder, converter)

    selectedOrder = arguments.Select

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
    
    __Wrapper__(TableErrorDisplay(), sourceFile, errorCodes, selectedOrder, tableConverterMethod)

    if(arguments.Export is not None):
        with CsvErrorDisplay(exportFile) as csvFile:
            __Wrapper__(csvFile, sourceFile, errorCodes, selectedOrder, exportConverterMethod)
