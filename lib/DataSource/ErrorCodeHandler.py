from ..Constants import Constants
from ..Utility import Utility
from ..Output import Out

def ErrorCodeFilter(errorCodeHandler):
    def __INTERNAL__(object, sourceFile, errorCodes, arguments):
        errorCodeHandler(object, sourceFile, [errorCode for errorCode in errorCodes if errorCode is not None], arguments)
    return __INTERNAL__


def ErrorCodeHandler(errorCodeHandlers):
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
        errorCodeHandlers(object, sourceFile, errorCodes, selectedOrder)
    return __INTERNAL__