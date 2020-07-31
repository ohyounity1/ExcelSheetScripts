import sys

import AppInitialization

from lib.Constants import Constants
from lib.Constants import SourceTypes
from lib.Constants import ActionTypes
from lib.Utility import Utility
from lib.DataSource import DataSources

# Program begins here
arguments = AppInitialization.ParseCommandLine()

from lib.Output import Out

Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Input files {0}'.format(arguments.Source))

mainSourceFile = arguments.Source[0]

Out.VerbosePrint(Out.Verbosity.LOW, 'Primary Source File Name: {0}'.format(mainSourceFile))

mainSourceResults = DataSources.RetrieveErrorCodes(mainSourceFile)

if(mainSourceResults is None):
    Out.ErrorPrint('There were no error codes found in {}!'.format(mainSourceFile))
    
actionType = None
secondarySourceResults = None

# We have a secondary source file
if(len(arguments.Source) > 1):

    secondarySourceFile = arguments.Source[1]
    
    Out.VerbosePrint(Out.VerbosityLow, 'Secondary Source File Name: {0}'.format(secondarySourceFile))
    
    secondarySourceResults, secondarySourceType = RetrieveSource(secondarySourceFile, output)

    if(secondarySourceResults is None):
        Out.ErrorPrint('There were no error codes found in {}!'.format(secondarySourceFile))
        
    actionType = ActionTypes.ActionType.DIFF
    
if(arguments.destination == 'Null'):
    exit()
    
if(arguments.destination == 'Prompt' and actionType != ActionTypes.ActionType.DIFF):
    print('Main Source Display {}'.format(mainSourceFile))
    ErrorCodeTableDisplay(mainSourceResults, mainSourceType, output)
    
    if(secondarySourceResults is not None):
        print('Secondary Source Display {}'.format(secondarySourceFile))
        ErrorCodeTableDisplay(secondarySourceResults, secondarySourceType, output)
        

if(actionType == ActionTypes.ActionType.DIFF):
    import DiffAction
    DiffAction.ActionDiffOnErrorLists(mainSourceResults, mainSourceFile, secondarySourceResults, secondarySourceFile)

# Helper methods below

def AddSelection(desiredSelection, selectedOrder, selectedItems):
    if(desiredSelection in selectedItems):
        selectedOrder.append(desiredSelection)
        
def ErrorCodeTableDisplay(errorCodes, sourceType, output):
    import TableDisplay
    
    selectionOfItems = Utility.IntrospectErrorCodes(errorCodes)
    selectedOrder = []
    
    AddSelection(Constants.ErrorNameProperty, selectedOrder, selectionOfItems)
    AddSelection(Constants.ErrorIdProperty, selectedOrder, selectionOfItems)
    AddSelection(Constants.ErrorModuleProperty, selectedOrder, selectionOfItems)
    AddSelection(Constants.ErrorTypeProperty, selectedOrder, selectionOfItems)
    AddSelection(Constants.ErrorDisplaysMsgProperty, selectedOrder, selectionOfItems)
    AddSelection(Constants.ErrorDisplayMsgProperty, selectedOrder, selectionOfItems)
        
    if(sourceType == SourceTypes.SourceType.EXCEL):
        selectedOrder.remove(Constants.ErrorModuleProperty)
    elif(sourceType == SourceTypes.SourceType.JSON):
        selectedOrder.remove(Constants.ErrorIdProperty)
    
    output.VerbosePrint(Out.VerbosityMedium, 'Items selected for display {}'.format(selectedOrder))
    
    TableDisplay.ErrorListToTableDisplay(errorCodes, selectedOrder)
