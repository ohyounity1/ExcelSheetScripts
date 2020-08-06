import argparse

from lib.Constants import Destinations
from lib.Constants import TableSelections
from lib.Constants import ActionTypes

from lib.Constants import Constants

from lib.Output import Out

def ParseCommandLine() -> argparse.Namespace:
    """Parse the command line options and return the resulting object
    
    Returns:
        TYPE: All the parsed arguments
    """
    # Setup the parser and take in the arguments
    parser = argparse.ArgumentParser(description='Retrieve data from Instrument Error Codes Spreadsheets.  This script can display the contents to the screen, or file, as well export various validations difference checking actions')
    # Multiple source files allowed
    parser.add_argument('-s', '--source', dest='Source', help='Source file name.  If .xls or .xlsx treated as Excel, .json treated as JSON', nargs='+', required=True)
    # The destination type for the output, can be prompt, CSV, JSON, Excel
    parser.add_argument('-d', '--destination', dest='Destination', help='Output destination.', default='prompt', choices=Destinations.Destinations.Values())
    parser.add_argument('-e', '--export', dest='Export', help='Type to export to, whether CSV or JSON', required=False, choices=Destinations.Exports.Values())
    # The columns to be displayed for the headers
    parser.add_argument('--select', dest='Select', help='Which columns to display in the tables', nargs='*', default=[], choices=TableSelections.TableSelections.Values())
    parser.add_argument('--diff-show-all', dest='DiffShowAll', help='Display all the items in the table for the diff, even those not different', action='store_true')
    parser.add_argument('--diff-actions', dest='DiffActions', help='The diff actions to run, can be several together: codes, msgs, types', nargs='*', default=[], choices=ActionTypes.DiffActions.Values())
    parser.add_argument('--validate-actions', dest='ValidateActions', help='The validate actions to run, can be several together: module, msg, hasmsg', nargs='*', default=[], choices=ActionTypes.ValidateActions.Values())
    parser.add_argument('-j', '--join', dest='JoinActions', help='Join the two table sources at the error code name, and provide the values from both tables as specified in the options', nargs='*', default=[], choices=ActionTypes.DiffActions.Values() + ActionTypes.ValidateActions.Values())
    # Redirect output to a log file
    parser.add_argument('--log', dest='Log', help='Indication to log all main output to the specified file', action='store_true', default=False)
    # Verbosity level is determined by typing -v multiple times
    parser.add_argument('-v', '--verbose', dest='Verbosity', help='Verbosity level.  Repeat for higher level... e.g. -vv will print with Medium Verbosity', action='count', default=0)

    arguments = parser.parse_args()

    return arguments

def InitializeApp(arguments: argparse.Namespace):
    """Initialize the application namesapce based on the provided arguments
    
    Args:
        arguments (TYPE): The command line arguments
    """
    # Only allow so many source files!   
    if(len(arguments.Source) > Constants.MaxValues.SourceArguments):
        Out.ErrorPrint('Too many source arguments!  Only {} are allowed...'.format(Constants.MaxValues.SourceArguments))
    
    # Make sure source files are all different
    if(len(arguments.Source) > 1 and arguments.Source[0] == arguments.Source[1]):
        Out.ErrorPrint('Error!  Source files are the same name! {}'.format(arguments.Source[0]))

    diffActionsLength = len(arguments.DiffActions)
    validateActionsLength = len(arguments.ValidateActions)
    joinActionsLength = len(arguments.JoinActions)

    argumentsGiven = [x for x in [diffActionsLength, validateActionsLength, joinActionsLength] if x > 0]

    if(len(argumentsGiven) > 1):
        Out.ErrorPrint('Error!  Can only do either --diff-actions, --validate-actions, --join separately, but not together... if you wish to combine the two, use --join')

    if(diffActionsLength > 0 and len(arguments.Source) <= 1):
        Out.ErrorPrint('Error!  Can not do a diff with only one file!')

    if(joinActionsLength > 0 and len(arguments.Source) <= 1):
        Out.ErrorPrint('Error!  Can not do a join with only one file!')

    # Max verbosity level
    arguments.Verbosity = min(arguments.Verbosity, Constants.MaxValues.VerbosityLevel)

    # Redirect output to a log
    if(arguments.Verbosity > 0):
        vlog = 'vlog'
        if(arguments.Log):
            Out.RegisterOutPlugin(vlog, Out.LogPrint('Verbosity.Log'))
            Out.VerbosePrint = Out.VerbosePrinter(arguments.Verbosity, vlog)
        else:
            Out.VerbosePrint = Out.VerbosePrinter(arguments.Verbosity, Destinations.Destinations.Prompt)

    if(arguments.Destination == Destinations.Destinations.File):
        Out.RegisterOutPlugin(Destinations.Destinations.File, Out.LogPrint('Output.Log'))

    Out.RegularPrint = Out.RegularPrinter(arguments.Destination)