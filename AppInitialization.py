import argparse

from lib.Constants import Constants
from lib.Constants import Colours

from lib.Output import Out

"""
    Summary: Parse the command line options
"""
def ParseCommandLine():
    # Setup the parser and take in the arguments
    parser = argparse.ArgumentParser(description='Retrieve data from Instrument Error Codes Spreadsheets!')
    # Multiple source files allowed
    parser.add_argument('-s', '--source', dest='Source', help='Source file name.  If .xls or .xlsx treated as Excel, .json treated as JSON', nargs='*', required=True)
    # Verbosity level is determined by typing -v multiple times
    parser.add_argument('-v', '--verbose', dest='Verbosity', help='Verbosity level.  Repeat for higher level... e.g. -vv will print with Medium Verbosity', action='count', default=0)
    # The columns to be displayed for the headers
    parser.add_argument('--select', dest='Select', help='Which columns to display in the tables', nargs='*', default=[])
    # Redirect output to a log file
    parser.add_argument('--vlog', dest='VLog', help='Indication to log verbose output to the specified file', default=None)
    parser.add_argument('--log', dest='Log', help='Indication to log all main output to the specified file', default=None)
    parser.add_argument('-a', '--action', dest='Action', help='The action to run, can be several together: DISPLAY, DIFF, EXPORT', nargs='*', default=['DISPLAY'])
    # The destination type for the output, can be prompt, CSV, JSON, Excel
    parser.add_argument('-d', '--destination', help='Destination file name.  If .xls or .xlsx treated as Excel, .json treated as JSON, prompt prints to prompt, Null for no output, CSV for CSV output', default='Prompt')

    arguments = parser.parse_args()

    # Only allow so many source files!    
    if(len(arguments.Source) > Constants.MaxSourceArguments):
        Out.ErrorPrint('Too many source arguments!  Only {} are allowed...'.format(Constants.MaxSourceArguments))
    
    # Make sure source files are all different
    if(len(arguments.Source) > 1 and arguments.Source[0] == arguments.Source[1]):
        Out.ErrorPrint('Error!  Source files are the same name! {}'.format(arguments.Source[0]))

    # Set the verbosity level
    Out.SetVerbosity(arguments.Verbosity)

    # Redirect output to a log
    if(arguments.VLog is not None):
        vlog = open(arguments.VLog, "a")
        Out.VerbosePrint = Out.VerbosePrinter(lambda o : vlog.write(o + '\n'))

    if(arguments.Log is not None):
        log = open(arguments.Log, "a")
        Out.RegularPrint = Out.RegularPrinter(lambda o : log.write(o + '\n'))

    for a in arguments.Action:
        print ('Action: {}'.format(a))
    return arguments