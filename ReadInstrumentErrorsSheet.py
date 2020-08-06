from pathlib import Path

from lib.Output import Out
from lib.Output import TableDisplay
from lib.Output import CsvDisplay

from lib.DataSource import ConversionMethods
from lib.DataSource import DataSources

from lib.Behaviors import DiffAnalyzers
from lib.Behaviors import ValidationClasses

import AppInitialization
import AppFactory
import Converters

def LineUpLists(listOne, listTwo, matchedCallback=None, unmatchedCallback=None):
    printCount = 0
    matchCount = 0
    mismatchCount = 0
    for errorCodeOne in listOne:
        errorCodeName = errorCodeOne.ErrorName
        foundErrorCodeInSecondList = False
        for errorCodeTwo in listTwo:
            if(errorCodeName == errorCodeTwo.ErrorName):
                if(matchedCallback is not None):
                    matchedCallback(errorCodeOne, errorCodeTwo)

                Out.VerbosePrint(Out.Verbosity.HIGH, f'{matchCount}/{printCount}: Found matching error code {errorCodeName}')
                matchCount += 1

                foundErrorCodeInSecondList = True
                break
        if(foundErrorCodeInSecondList == False):
            Out.VerbosePrint(Out.Verbosity.HIGH, f'{mismatchCount}/{printCount}: Not finding error code {errorCodeName} in the second list...')
            mismatchCount += 1

            if(unmatchedCallback is not None):
                unmatchedCallback(errorCodeOne)
        printCount += 1

def ArrangeErrorCodesInSameOrder(listOne, listTwo):
    firstOrder = []
    secondOrder = []

    def __MATCH__(one, two):
        firstOrder.append(one)
        secondOrder.append(two)

    def __NO_MATCH__(lOne, lTwo):
        def __INTERNAL__(one):
            lOne.append(one)
            lTwo.append(None)
        return __INTERNAL__

    Out.VerbosePrint(Out.Verbosity.LOW, f'Before re-arranging order, first list {len(listOne)} long and second list is {len(listTwo)} long')
    LineUpLists(listOne, listTwo, matchedCallback=__MATCH__, unmatchedCallback=__NO_MATCH__(firstOrder, secondOrder))

    Out.VerbosePrint(Out.Verbosity.LOW, f'After first re-arranging order, first list {len(firstOrder)} long and second list is {len(secondOrder)} long')
    LineUpLists(listTwo, listOne, unmatchedCallback=__NO_MATCH__(secondOrder, firstOrder))

    Out.VerbosePrint(Out.Verbosity.LOW, f'After re-arranging order, first list {len(firstOrder)} long and second list is {len(secondOrder)} long')
    Out.VerbosePrint(Out.Verbosity.LOW, f'After re-arranging order, original first list {len(listOne)} long and original second list is {len(listTwo)} long')

    return firstOrder, secondOrder

def main(arguments):
    
    AppInitialization.InitializeApp(arguments)
    
    behaviors = AppFactory.AppFactory(arguments)

    Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Input files {0}'.format(arguments.Source))
    
    mainSourceFile = arguments.Source[0]
    
    # Retrieve error codes from the main source file
    mainSourceResults = ConversionMethods.DataSourceConversion(mainSourceFile)
    
    secondarySourceFile = None
    secondarySourceResults = None
    
    sourceCenters = list()
    
    # We have a secondary source file
    if(len(arguments.Source) > 1):
        secondarySourceFile = arguments.Source[1]
        secondarySourceResults = ConversionMethods.DataSourceConversion(secondarySourceFile)

        firstOrder, secondOrder = ArrangeErrorCodesInSameOrder(mainSourceResults, secondarySourceResults)

        sourceCenters.append(DataSources.SourceCenter(SourceName=mainSourceFile, SourceResults=firstOrder))
        sourceCenters.append(DataSources.SourceCenter(SourceName=secondarySourceFile, SourceResults=secondOrder))
    else:
        sourceCenters.append(DataSources.SourceCenter(SourceName=mainSourceFile, SourceResults=mainSourceResults))
    
    # Only display the source file contents to the output display IF NOT doing any diff/validation actions
    behaviors.ReportAndExportBehavior(sourceCenters, arguments)
    
    if(len(arguments.DiffActions) > 0 and len(sourceCenters) > 1):
        for action in arguments.DiffActions:
            differs = DiffAnalyzers.AnalyzerFactory(sourceCenters[0].SourceName, sourceCenters[1].SourceName, arguments, action)
            differs(zip(sourceCenters[0].SourceResults, sourceCenters[1].SourceResults))
    
    if(len(arguments.ValidateActions) > 0):
        for validation in arguments.ValidateActions:
            mainValidator = ValidationClasses.ValidatorFactory(sourceCenters[0].SourceName, arguments, validation)
            mainValidator(sourceCenters[0].SourceResults)

            if(secondarySourceResults is not None):
                secondaryValidator = ValidationClasses.ValidatorFactory(sourceCenters[1].SourceName, arguments, validation, 2)
                secondaryValidator(sourceCenters[1].SourceResults)

    if(len(arguments.JoinActions) > 0 and secondarySourceResults != None):
        for joinAction in arguments.JoinActions:
            joiner = JoinAnalyzers.JoinFactory(mainSourceFile, secondarySourceFile, arguments, action)
            joiner(mainSourceResults, secondarySourceResults)

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    # Program begins here, parse the command line options
    arguments = AppInitialization.ParseCommandLine()

    main(arguments)