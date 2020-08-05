from lib.Output import Out
from lib.DataSource import DataSources
from lib.Utility import Utility
from lib.Constants import Constants
from lib.Constants import Destinations

from lib.Output import TableDisplay
from lib.Output import CsvDisplay

def ErrorCodeHandler(errorCodeHandlers):
    errorCodeHandlersCaptures = errorCodeHandlers
    def __INTERNAL__(object, sourceFile, errorCodes, arguments):
        __DefaultRemoveFromSelection__ = {
           '.xls' : [Constants.ErrorModuleProperty],
           '.xlsx': [Constants.ErrorModuleProperty],
           '.json': [Constants.ErrorIdProperty] }
        
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
                Constants.ErrorDisplayMsgProperty], lambda e: e not in __DefaultRemoveFromSelection__[extension])
        
        Out.VerbosePrint(Out.Verbosity.LOW, 'Items selected for display {}'.format(selectedOrder))
        #for handlers in errorCodeHandlersCaptures:
        #    handlers.PrintHeader(f'Source Display for {sourceFile}')
        #    handlers.HandleErrorCode(errorCodes, selectedOrder, handlers.ConvertData)
        errorCodeHandlers(object, sourceFile, errorCodes, selectedOrder)
    return __INTERNAL__

class SourceStrategyComposite:
    def __init__(self, strategies):
        self.Strategies = strategies
    @ErrorCodeHandler
    def Execute(self, sourceFile, errorCodes, selectedOrder):
        for strategy in self.Strategies:
            strategy.PrintHeader(f'Source Display for {sourceFile}')
            strategy.HandleErrorCode(errorCodes, selectedOrder, strategy.ConvertData)    