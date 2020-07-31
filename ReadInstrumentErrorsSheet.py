import sys

import AppInitialization

from lib.Constants import Constants
from lib.Constants import SourceTypes
from lib.Constants import ActionTypes
from lib.Utility import Utility
from lib.DataSource import DataSources
from lib.Output import ErrorCodeDisplay

def RetrieveAllResults(sourceFile):
    Out.VerbosePrint(Out.Verbosity.LOW, 'Source File Name: {0}'.format(sourceFile))

    errorCodes = DataSources.RetrieveErrorCodes(mainSourceFile)

    if(errorCodes is None or len(errorCodes) == 0):
        Out.ErrorPrint('There were no error codes found in {}!'.format(sourceFile))

    return errorCodes

__DefaultSelection__ = {
    '.xls' : [Constants.ErrorModuleProperty],
    '.xlsx': [Constants.ErrorModuleProperty],
    '.json': [Constants.ErrorIdProperty]
}

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

def ErrorCodeTableDisplay(sourceFile, errorCodes, selectedColumns):
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
    
    TableDisplay.ErrorListToTableDisplay(errorCodes, selectedOrder, ConvertDisplayMsg)

# Program begins here, parse the command line options
arguments = AppInitialization.ParseCommandLine()

from lib.Output import Out

Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Input files {0}'.format(arguments.Source))

mainSourceFile = arguments.Source[0]

# Retrieve error codes from the main source file
mainSourceResults = RetrieveAllResults(mainSourceFile)

secondarySourceResults = None

# We have a secondary source file
if(len(arguments.Source) > 1):
    secondarySourceFile = arguments.Source[1]
    secondarySourceResults = RetrieveAllResults(secondarySourceFile)
    
if(arguments.destination == 'Null'):
    exit()
    
if(arguments.destination == 'Prompt'):
    # Print all results to output
    Out.RegularPrint('Main Source Display {}'.format(mainSourceFile))
    
    ErrorCodeTableDisplay(mainSourceFile, mainSourceResults, arguments.Select)
    
    if(secondarySourceResults is not None):
        Out.RegularPrint('Secondary Source Display {}'.format(secondarySourceFile))
        extension = Path(secondarySourceFile).suffix
        ErrorCodeTableDisplay(secondarySourceFile, secondarySourceResults, arguments.Select)

if(actionType == ActionTypes.ActionType.DIFF):
    import DiffAction
    DiffAction.ActionDiffOnErrorLists(mainSourceResults, mainSourceFile, secondarySourceResults, secondarySourceFile)

