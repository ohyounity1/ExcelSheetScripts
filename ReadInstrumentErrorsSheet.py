import sys
import argparse

from lib.Output import Out
from lib.Output import Table

from lib.ErrorCodes import ErrorCode    

output = Out.Out()

parser = argparse.ArgumentParser(description='Retrieve data from Instrument Error Codes Spreadsheets!')
parser.add_argument('-s', '--source', dest='Source', help='Source file name.  If .xls or .xlsx treated as Excel, .json treated as JSON', nargs='+', required=True)
parser.add_argument('-v', '--verbose', dest='Verbosity', help='Verbosity level.  Repeat for higher level... e.g. -vv will print with Medium Verbosity', action='count', default=0)

parser.add_argument('-d', '--destination', help='Destination file name.  If .xls or .xlsx treated as Excel, .json treated as JSON, prompt prints to prompt', default='Prompt')

arguments = parser.parse_args()

if(len(arguments.Source) > 2):
    output.Error('Too many source arguments!  Only 2 are allowed...')
    
if(len(arguments.Source) > 1 and arguments.Source[0] == arguments.Source[1]):
    output.Error('Error!  Source files are the same name! {}'.format(arguments.Source[0]))

output.Verbosity = arguments.Verbosity
output.Verbose(Out.VerbosityMedium, 'Input files {0}'.format(arguments.Source))

from pathlib import Path

errorCodeListing1 = None
errorCodeListing2 = None

import ExcelConversion

errorCodeListing1 = None

mainSourceFile = arguments.Source[0]

if(Path(mainSourceFile).suffix == '.xls' or Path(mainSourceFile).suffix == '.xlsx'):
    errorCodeListing1 = ExcelConversion.ExcelSheetErrorCodeListing(mainSourceFile, output)

if(errorCodeListing1 is None):
    output.Error('There were no error codes found in {}!'.format(mainSourceFile))
    
if(arguments.destination == 'Prompt'):
    tabularFormat = [ ]
    largestColumns = [0,0,0,0,0]
    headers = []
    for header in vars(errorCodeListing1[0]):
        headers.append(header)
    
    tabularFormat.append(headers)
    for ec in errorCodeListing1:
        if(len(ec.ErrorDisplayMsg) > 0):
            tabularFormat.append([ec.ErrorName, ec.ErrorId, ec.ErrorType, ec.ErrorDisplaysMsg, '{}...'.format(ec.ErrorDisplayMsg[0:30])])
        else:
            tabularFormat.append([ec.ErrorName, ec.ErrorId, ec.ErrorType, ec.ErrorDisplaysMsg, ''])
        larger = max(len(ec.ErrorName), len(headers[0]))
        if(larger > largestColumns[0]):
            largestColumns[0] = larger + 1
        larger = max(len(str(ec.ErrorId)), len(headers[1]))
        if(larger > largestColumns[1]):
            largestColumns[1] = larger + 1
        larger = max(len(ec.ErrorType), len(headers[2]))
        if(larger > largestColumns[2]):
            largestColumns[2] = larger + 1
        larger = max(len(str(ec.ErrorDisplaysMsg)), len(headers[3]))
        if(larger > largestColumns[3]):
            largestColumns[3] = larger + 1
        larger = max(len(str(ec.ErrorDisplayMsg[0:30]))+3, len(headers[4]))
        if(larger > largestColumns[4]):
            largestColumns[4] = larger + 1
    
    print('|{}|{}|{}|{}|{}|'.format('-' * (largestColumns[0]), '-' * (largestColumns[1]),  '-' * (largestColumns[2]),  '-' * (largestColumns[3]),  '-' * (largestColumns[4])))
    print('%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2], largestColumns[3], largestColumns[4]) % ('|', headers[0], '|', headers[1], '|', headers[2], '|', headers[3], '|', headers[4], '|'))
    print('|{}|{}|{}|{}|{}|'.format('-' * (largestColumns[0]), '-' * (largestColumns[1]), '-' * (largestColumns[2]), '-' * (largestColumns[3]), '-' * (largestColumns[4])))
    for ec in tabularFormat:
        print('%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c%-{}s%c'.format(largestColumns[0], largestColumns[1], largestColumns[2], largestColumns[3], largestColumns[4]) % ('|', ec[0], '|', ec[1], '|', ec[2], '|', ec[3], '|', ec[4], '|'))
    print('|{}|{}|{}|{}|{}|'.format('-' * (largestColumns[0]), '-' * (largestColumns[1]), '-' * (largestColumns[2]), '-' * (largestColumns[3]), '-' * (largestColumns[4])))
    