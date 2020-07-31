import sys
import difflib

import AppInitialization

from lib.Constants import Constants
from lib.Constants import ActionTypes
from lib.Utility import Utility
from lib.DataSource import DataSources

import Helper
import TableDisplay

# Program begins here, parse the command line options
arguments = AppInitialization.ParseCommandLine()

from lib.Output import Out

Out.VerbosePrint(Out.Verbosity.MEDIUM, 'Input files {0}'.format(arguments.Source))

mainSourceFile = arguments.Source[0]
# Retrieve error codes from the main source file
mainSourceResults = Helper.RetrieveAllResults(mainSourceFile)

secondarySourceFile = None
secondarySourceResults = None

# We have a secondary source file
if(len(arguments.Source) > 1):
    secondarySourceFile = arguments.Source[1]
    secondarySourceResults = Helper.RetrieveAllResults(secondarySourceFile)
    
if(arguments.destination == 'Null'):
    exit()
    
if('Display' in arguments.Action):
    Helper.ErrorCodeTableDisplay(mainSourceFile, mainSourceResults, arguments.destination, arguments.Select)
    
    if(secondarySourceResults is not None):
        Helper.ErrorCodeTableDisplay(secondarySourceFile, secondarySourceResults, arguments.destination, arguments.Select)
elif(arguments.destination == 'CSV' and 'Display' in arguments.Action):
    with open('ErrorCodesListing.csv', 'w') as csvFile:

        # Print all results to output
        csvFile.write('Main Source Display {}'.format(mainSourceFile))
    
        csvFile.write(f'\n')
    
        if(secondarySourceResults is not None):
            Out.RegularPrint('Secondary Source Display {}'.format(secondarySourceFile))
            Helper.ErrorCodeTableDisplay(secondarySourceFile, secondarySourceResults, arguments.Select)


if(len(arguments.Action) > 0 and secondarySourceResults != None):
    import DiffAction
    for action in arguments.Action:
        if(action == 'Diff-Codes' or action == 'Diff-All'):
            diffs = DiffAction.ActionDiffErrorCodes(Utility.Tie(mainSourceResults, secondarySourceResults), Utility.Tie(mainSourceFile, secondarySourceFile))
            if(len(diffs) > 0):
                if(arguments.destination == 'Prompt'):
                    Out.RegularPrint('ERROR CODE SUMMARY:::::')
                    Out.RegularPrint('--LeftSource = \n---- Errors in {}, but not in {}\n--RightSource = \n---- Errors in {}, but not in {}\n--TotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, secondarySourceFile, mainSourceFile, len(diffs)))
                    TableDisplay.ErrorListToTableDisplay(diffs, ['ErrorCodeLeft', 'ErrorCodeRight'])
                elif(arguments.destination == 'CSV'):
                    with open('ErrorCodesDiff.csv', 'w') as csvFile:
                        csvFile.write('ERROR CODE SUMMARY:::::')
                        csvFile.write('\nLeftSource = \n\tErrors in {}, but not in {}\nRightSource = \n\tErrors in {}, but not in {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, secondarySourceFile, mainSourceFile, len(diffs)))
                        csvFile.write('\nLeftSource, RightSource')
                        for diff in diffs:
                            csvFile.write('\n{},{}'.format(diff.ErrorCodeLeft, diff.ErrorCodeRight))
        if(action == 'Diff-Types' or action == 'Diff-All'):
            diffs = DiffAction.ActionDiffOnErrorLists(mainSourceResults, secondarySourceResults, action, arguments.DiffShowAll)
            if(len(diffs) > 0):
                if(arguments.destination == 'Prompt'):
                    Out.RegularPrint('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, len(diffs)))
                    TableDisplay.ErrorListToTableDisplay(diffs, ['ErrorCodeName', 'FirstValue', 'SecondValue'], Helper.ConvertErrorTypeDisplayMsg)
                elif(arguments.destination == 'CSV'):
                    with open('ErrorTypesDiff.csv', 'w') as csvFile:
                        csvFile.write('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, len(diffs)))
                        csvFile.write('\nErrorCodeName,FirstValue, SecondValue')
                        for diff in diffs:
                            csvFile.write('\n{},{},{}'.format(diff.ErrorCodeName, str(diff.FirstValue), str(diff.SecondValue)))
        if(action == 'Diff-Msgs' or action == 'Diff-All'):
            diffs = DiffAction.ActionDiffOnErrorLists(mainSourceResults, secondarySourceResults, action, arguments.DiffShowAll)
            if(len(diffs) > 0):
                csvFile = None
                if(arguments.destination == 'Prompt'):
                    Out.RegularPrint('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, len(diffs)))
                elif(arguments.destination == 'CSV'):
                    csvFile = open('ErrorMsgsDiff.csv', 'w')
                    csvFile.write('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(mainSourceFile, secondarySourceFile, len(diffs)))
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
                if(arguments.destination == 'Prompt'):
                    Out.RegularPrint('\n{}\n--Summary:{}\n----{}\n------{}\n----{}\n------{}\n'.format(x.ErrorCodeName, reasonString, mainSourceFile, first, secondarySourceFile, second))
                elif(arguments.destination == 'CSV'):
                    csvFile.write('\n{},{},{},{}'.format(x.ErrorCodeName, reasonString, first, second))

            if(csvFile is not None):
                csvFile.close()


