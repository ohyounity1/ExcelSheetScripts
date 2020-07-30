import sys
import argparse

from lib.Constants import Constants
from lib.Constants import SourceTypes
from lib.Constants import ActionTypes
from lib.Utility import Utility

def RetrieveSource(filePath, output):
    from pathlib import Path
    import ExcelConversion
    import JsonConversion

    if(Path(filePath).suffix in Constants.SupportedExcelExtensions):
        return ExcelConversion.ExcelSheetErrorCodeListing(filePath, output), SourceTypes.SourceType.EXCEL
    elif(Path(filePath).suffix in Constants.SupportedJsonExtensions):
        return JsonConversion.JsonFileErrorCodeListing(filePath, output), SourceTypes.SourceType.JSON

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
    
    output.Verbose(Out.VerbosityMedium, 'Items selected for display {}'.format(selectedOrder))
    
    TableDisplay.ErrorListToTableDisplay(errorCodes, selectedOrder)
    
def ParseCommandLine(output):
    parser = argparse.ArgumentParser(description='Retrieve data from Instrument Error Codes Spreadsheets!')
    parser.add_argument('-s', '--source', dest='Source', help='Source file name.  If .xls or .xlsx treated as Excel, .json treated as JSON', nargs='+', required=True)
    parser.add_argument('-v', '--verbose', dest='Verbosity', help='Verbosity level.  Repeat for higher level... e.g. -vv will print with Medium Verbosity', action='count', default=0)

    parser.add_argument('-d', '--destination', help='Destination file name.  If .xls or .xlsx treated as Excel, .json treated as JSON, prompt prints to prompt, Null for no output', default='Prompt')

    arguments = parser.parse_args()
    
    if(len(arguments.Source) > Constants.MaxSourceArguments):
        output.Error('Too many source arguments!  Only {} are allowed...'.format(Constants.MaxSourceArguments))
    
    if(len(arguments.Source) > 1 and arguments.Source[0] == arguments.Source[1]):
        output.Error('Error!  Source files are the same name! {}'.format(arguments.Source[0]))

    return arguments
    

    
from lib.Output import Out

output = Out.Out()

arguments = ParseCommandLine(output)

output.Verbosity = arguments.Verbosity
output.Verbose(Out.VerbosityMedium, 'Input files {0}'.format(arguments.Source))

mainSourceFile = arguments.Source[0]

output.Verbose(Out.VerbosityLow, 'Primary Source File Name: {0}'.format(mainSourceFile))

mainSourceResults, mainSourceType = RetrieveSource(mainSourceFile, output)

if(mainSourceResults is None):
    output.Error('There were no error codes found in {}!'.format(mainSourceFile))
    
actionType = None

# We have a secondary source file
if(len(arguments.Source) > 1):

    secondarySourceFile = arguments.Source[1]
    
    output.Verbose(Out.VerbosityLow, 'Secondary Source File Name: {0}'.format(secondarySourceFile))
    
    secondarySourceResults, secondarySourceType = RetrieveSource(secondarySourceFile, output)

    if(secondarySourceResults is None):
        output.Error('There were no error codes found in {}!'.format(secondarySourceFile))
        
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