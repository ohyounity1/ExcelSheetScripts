import sys

from pathlib import Path
from collections import namedtuple

import AppInitialization

from lib.Constants import Constants
from lib.Constants import ActionTypes
from lib.Constants import Destinations
from lib.Utility import Utility
from lib.DataSource import ConversionMethods
from lib.Output import TableDisplay
from lib.Output import CsvDisplay
from lib.DataSource import DataSources

import Helper
import DiffAnalyzers
import Converters

# Program begins here, parse the command line options
arguments = AppInitialization.ParseCommandLine()

from lib.Output import Out

Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Input files {0}'.format(arguments.Source))

mainSourceFile = arguments.Source[0]

# Retrieve error codes from the main source file
mainSourceResults = ConversionMethods.DataSourceConversion(mainSourceFile)

secondarySourceFile = None
secondarySourceResults = None

sourceCenters = list()
sourceCenters.append(DataSources.SourceCenter(SourceName=mainSourceFile, SourceResults=mainSourceResults))

# We have a secondary source file
if(len(arguments.Source) > 1):
    secondarySourceFile = arguments.Source[1]
    secondarySourceResults = ConversionMethods.DataSourceConversion(secondarySourceFile)
    sourceCenters.append(DataSources.SourceCenter(SourceName=secondarySourceFile, SourceResults=secondarySourceResults))

# Only display the source file contents to the output display IF NOT doing any diff/validation actions
if(len(arguments.DiffActions) == 0):
    for sourceCenter in sourceCenters:
        with DataSources.ExportSources() as exportSources:
            sourceStrategies = list()
            sourceStrategies.append(DataSources.SourceStrategy(PrintHeader=Out.RegularPrint, 
                HandleErrorCode=TableDisplay.ErrorListToTableDisplay,
                ConvertData=Converters.ConvertTableDisplayMsg))
        
            if(arguments.Export is not None):
                exportFileName = f'{Path(sourceCenter.SourceName).stem}_Export.csv'
                exportFile = open(exportFileName, 'w')
                exportSources += exportFile
                sourceStrategies.append(DataSources.SourceStrategy(PrintHeader=exportFile.write, 
                    HandleErrorCode=lambda errors, selections, converter: CsvDisplay.ErrorListToCSVDisplay(exportFile, errors, selections, converter),
                    ConvertData=Converters.ConvertCSVOutput))
            strategies = Helper.SourceStrategyComposite(sourceStrategies)
            strategies.Execute(sourceCenter.SourceName, sourceCenter.SourceResults, arguments)

if(len(arguments.DiffActions) > 0 and secondarySourceResults != None):

    for action in arguments.DiffActions:
        differs = DiffAnalyzers.AnalyzerFactory(mainSourceFile, secondarySourceFile, arguments, action)
        differs.RunAnalysis(mainSourceResults, secondarySourceResults)

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




