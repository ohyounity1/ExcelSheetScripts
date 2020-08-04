import sys
import difflib

from pathlib import Path
from collections import namedtuple

import AppInitialization

from lib.Constants import Constants
from lib.Constants import ActionTypes
from lib.Constants import Destinations
from lib.Utility import Utility
from lib.DataSource import DataSources
from lib.Output import TableDisplay
from lib.Output import CsvDisplay

import Helper

# Program begins here, parse the command line options
arguments = AppInitialization.ParseCommandLine()

from lib.Output import Out

def ConvertErrorTypeDiffDisplayMsg(name, data):
    if(name == 'FirstValue' or name == 'SecondValue'):
        return str(data)
    return data

def ConvertTableDisplayMsg(name, data):
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

def ConvertCSVOutput(name, data):
    if(name == 'ErrorDisplayMsg'):
        data = data.replace('"', '""')
        rowString = f'"{data}"'
    else:
        rowString = f'{data}'
    return rowString

class DiffClass:
    def Write(self, msg):
        pass
    def Diff(diffs, properties):
        pass

class CompositeDiffClass(DiffClass):
    def __init__(self, composed):
        self.Composed = composed
    def Write(self, msg):
        for c in self.Composed:
            c.Write(msg)
    def Diff(self, diffs, properties):
        for c in self.Composed:
            c.Diff(diffs, properties)

class SingleDiffClassBase(DiffClass):
    def __init__(self, formatter, output, converter=None):
        self.Formatter = formatter
        self.Output = output
        self.Converter = converter
    def Write(self, msg):
        msg = self.Formatter(msg)
        self.Output(msg)

class TableDiff(SingleDiffClassBase):
    def __init__(self, converter=None):
        def __FORMATTER__(msg):
            return msg
        super().__init__(__FORMATTER__, Out.RegularPrint, converter)
        self.Converter = converter
    def Diff(self, diffs, properties):
        TableDisplay.ErrorListToTableDisplay(diffs, properties, self.Converter)

class CsvDiff(SingleDiffClassBase):
    def __init__(self, fileName, converter=None):
        def __FORMATTER__(msg):
            return f'\n{msg}'
        self.File = open(fileName + '.csv', 'w')
        super().__init__(__FORMATTER__, self.File.write, converter)
    def Diff(self, diffs, properties):
        CsvDisplay.ErrorListToCSVDisplay(self.File, diffs, properties, self.Converter)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback ):
        self.File.close()

def DiffDisplay(differ, diffs, properties, msgs):
    for msg in msgs:
        differ.Write(msg)
    differ.Diff(diffs, properties)

def MakeTableDiff(action):
    tableDiff = TableDiff()
    if(action == 'types'):
        tableDiff = TableDiff(ConvertErrorTypeDiffDisplayMsg)
    return tableDiff

def MakeCsvDiff(action):
    tableDiff = CsvDiff(action)
    if(action == 'types'):
        tableDiff = CsvDiff(action, ConvertErrorTypeDiffDisplayMsg)
    return tableDiff

Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Input files {0}'.format(arguments.Source))

mainSourceFile = arguments.Source[0]
# Retrieve error codes from the main source file
mainSourceResults = Helper.RetrieveAllResults(mainSourceFile)

secondarySourceFile = None
secondarySourceResults = None

sourceCenters = list()
sourceCenters.append(DataSources.SourceCenter(SourceName=mainSourceFile, SourceResults=mainSourceResults))

# We have a secondary source file
if(len(arguments.Source) > 1):
    secondarySourceFile = arguments.Source[1]
    secondarySourceResults = Helper.RetrieveAllResults(secondarySourceFile)
    sourceCenters.append(DataSources.SourceCenter(SourceName=secondarySourceFile, SourceResults=secondarySourceResults))

# Only display the source file contents to the output display IF NOT doing any diff/validation actions
if(len(arguments.DiffActions) == 0):
    for sourceCenter in sourceCenters:
        with DataSources.ExportSources() as exportSources:
            sourceStrategies = list()
            sourceStrategies.append(DataSources.SourceStrategy(PrintHeader=Out.RegularPrint, 
                HandleErrorCode=TableDisplay.ErrorListToTableDisplay,
                ConvertData=ConvertTableDisplayMsg))
        
            if(arguments.Export is not None):
                exportFileName = f'{Path(sourceCenter.SourceName).stem}_Export.csv'
                exportFile = open(exportFileName, 'w')
                exportSources += exportFile
                sourceStrategies.append(DataSources.SourceStrategy(PrintHeader=exportFile.write, 
                    HandleErrorCode=lambda errors, selections, converter: CsvDisplay.ErrorListToCSVDisplay(exportFile, errors, selections, converter),
                    ConvertData=ConvertCSVOutput))
            Helper.ErrorCodeHandler(sourceStrategies)(sourceCenter.SourceName, sourceCenter.SourceResults, arguments)

if(len(arguments.DiffActions) > 0 and secondarySourceResults != None):
    differs = dict()
    if(arguments.Destination != 'null' and arguments.Export == 'csv'):
        for action in arguments.DiffActions:
            tableDiff = MakeTableDiff(action)
            differs[action] = CompositeDiffClass([MakeTableDiff(action), MakeCsvDiff(action)])
    elif(arguments.Export == 'csv'):
        differs = {action: MakeCsvDiff(action) for differ in differs}
    elif(arguments.Destination != 'null'):
        for action in arguments.DiffActions:
            tableDiff = MakeTableDiff(action)
            differs[action] = tableDiff
    else:
        exit()
    import DiffAction

    for action in arguments.DiffActions:
        if(action == 'codes'):
            diffs = DiffAction.ActionDiffErrorCodes(Utility.Tie(mainSourceResults, secondarySourceResults), Utility.Tie(mainSourceFile, secondarySourceFile))
            if(len(diffs) > 0):
                msgs = ['ERROR CODE SUMMARY:::::',
                    '\n\tLeftSource = \n\t\tErrors in {}, but not in {}\n\tRightSource = \n\t\tErrors in {}, but not in {}\n\tTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, secondarySourceFile, mainSourceFile, len(diffs))]
                DiffDisplay(differs[action], diffs, ['ErrorCodeLeft', 'ErrorCodeRight'], msgs)
        if(action == 'types'):
            diffs, count = DiffAction.ActionDiffOnErrorLists(mainSourceResults, secondarySourceResults, action, arguments.DiffShowAll)
            if(len(diffs) > 0):
                msgs = ['FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, count)]
                DiffDisplay(differs[action], diffs, ['ErrorCodeName', 'FirstValue', 'SecondValue'], msgs)
        if(action == 'msgs'):
            diffs, count= DiffAction.ActionDiffOnErrorLists(mainSourceResults, secondarySourceResults, action, arguments.DiffShowAll)
            if(len(diffs) > 0):
                csvFile = None
                if(arguments.Destination != 'null'):
                    Out.RegularPrint('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, count))
                if(arguments.Export == 'csv'):
                    csvFile = open(action + '.csv', 'w')
                    csvFile.write('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, count))
                    csvFile.write('\nErrorCode, Reason, FirstValue, SecondValue')
            for x in diffs:
                first = x.FirstValue
                second = x.SecondValue
                reasonString = ''
                if(len(first) == 0):
                    reasonString = 'First display msg is empty!'
                elif(len(second) == 0):
                    reasonString = 'Second display msg is empty!'
                else:
                    for i,s in enumerate(difflib.ndiff(first, second)):
                        if s[0]==' ': continue
                        elif s[0]=='-':
                            reasonString += (u' Delete "{}" from position {} '.format(s[-1],i))
                            if(i < len(first)):
                                first = first[:i] + '[' + first[i] + ']' + first[i+1:]
                        
                            if(i < len(second)):
                                second = second[:i] + '[' + second[i] + ']' + second[i+1:]
                            break
                        elif s[0]=='+':
                            reasonString += (u' Add "{}" to position {} '.format(s[-1],i))    
                            if(i < len(first)):
                                first = first[:i] + '[' + first[i] + ']' + first[i+1:]
                        
                            if(i < len(second)):
                                second = second[:i] + '[' + second[i] + ']' + second[i+1:]
                            break
                if(arguments.Destination != 'null'):
                    Out.RegularPrint('\n{}\n--Summary:{}\n----{}\n------{}\n----{}\n------{}\n'.format(x.ErrorCodeName, reasonString, mainSourceFile, first, secondarySourceFile, second))
                if(arguments.Export == 'csv'):
                    csvFile.write('\n{},{},{},{}'.format(x.ErrorCodeName, reasonString, first, second))

            if(csvFile is not None):
                csvFile.close()

if(len(arguments.ValidateActions) > 0):
    for validation in arguments.ValidateActions:
        if(validation == ActionTypes.ValidateActions.MODULES):
            validateList = []

            if(Path(mainSourceFile).suffix == '.json'):
                validateList = mainSourceResults
            elif(Path(secondarySourceFile).suffix == '.json'):
                validateList = secondarySourceResults

            for ec in validateList:
                errorCodeName = ec.ErrorName
                errorCodeModule = ec.ErrorModule

                if('HANDLER' in errorCodeName):
                    if(errorCodeModule != 'PlateHandler'):
                        print(f'Suggest making {errorCodeName} module be PlateHandler and not {errorCodeModule}')
                elif('DG' in errorCodeName):
                    if(errorCodeModule != 'DG'):
                        print(f'Suggest making {errorCodeName} module be DG and not {errorCodeModule}')
                elif('DR' in errorCodeName):
                    if(errorCodeModule != 'DR'):
                        print(f'Suggest making {errorCodeName} module be DR and not {errorCodeModule}')




