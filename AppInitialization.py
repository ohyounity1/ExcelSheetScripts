import argparse

from lib.Constants import Constants
from lib.Constants import Colours

from lib.Output import Out

def ParseCommandLine():
    parser = argparse.ArgumentParser(description='Retrieve data from Instrument Error Codes Spreadsheets!')
    parser.add_argument('-s', '--source', dest='Source', help='Source file name.  If .xls or .xlsx treated as Excel, .json treated as JSON', nargs='+', required=True)
    parser.add_argument('-v', '--verbose', dest='Verbosity', help='Verbosity level.  Repeat for higher level... e.g. -vv will print with Medium Verbosity', action='count', default=0)
    parser.add_argument('--select', dest='Selection', help='Which columns to display in the tables', nargs='*')
    parser.add_argument('--log', dest='Log', help='Indication to log to the specified file', default=None)
    parser.add_argument('-d', '--destination', help='Destination file name.  If .xls or .xlsx treated as Excel, .json treated as JSON, prompt prints to prompt, Null for no output, CSV for CSV output', default='Prompt')

    arguments = parser.parse_args()
    
    if(len(arguments.Source) > Constants.MaxSourceArguments):
        Out.ErrorPrint('Too many source arguments!  Only {} are allowed...'.format(Constants.MaxSourceArguments))
    
    if(len(arguments.Source) > 1 and arguments.Source[0] == arguments.Source[1]):
        Out.ErrorPrint('Error!  Source files are the same name! {}'.format(arguments.Source[0]))

    Out.SetVerbosity(arguments.Verbosity)

    if(arguments.Log is not None):
        log = open(arguments.Log, "a")
        Out.VerbosePrint = Out.VerbosePrinter(lambda o : log.write(o + '\n'))
    return arguments