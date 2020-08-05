import sys
import os

from dataclasses import dataclass
from dataclasses import field

import ReadInstrumentErrorsSheet

if(len(sys.argv) < 2):
	print('Please provide the two source files!')
	exit()

fileOne = sys.argv[1]
fileTwo = sys.argv[2]
verbose = 0

if(len(sys.argv) > 3):
	verbose = sys.argv[3]

@dataclass
class Arguments:
	Source: [str]
	Destination: str = 'null'
	Export: str = 'csv'
	Select: [str] = field(default_factory=list)
	DiffShowAll: bool = True
	DiffActions: [str] = field(default_factory=list)
	ValidateActions: [str] = field(default_factory=list)
	Log : bool = False
	Verbosity: int = 0


# Export the two files to csv first
arguments = Arguments(Source=[fileOne, fileTwo], Verbosity=verbose)
ReadInstrumentErrorsSheet.main(arguments)

# Export all diffs to csv next
arguments = Arguments(Source=[fileOne, fileTwo], Verbosity=verbose, DiffActions=['codes', 'types', 'msgs'])
ReadInstrumentErrorsSheet.main(arguments)

# Export all validations to csv next
arguments = Arguments(Source=[fileOne], Verbosity=verbose, ValidateActions=['modules', 'hasmsg'])
ReadInstrumentErrorsSheet.main(arguments)
try:
	os.rename('modules_validation.csv', 'first_modules_validation.csv')
except:
	pass

try:
	os.rename('hasmsg_validation.csv', 'first_hasmsg_validation.csv')
except:
	pass

arguments = Arguments(Source=[fileTwo], Verbosity=verbose, ValidateActions=['modules', 'hasmsg'])
ReadInstrumentErrorsSheet.main(arguments)

try:
	os.rename('modules_validation.csv', 'second_modules_validation.csv')
except:
	pass

try:
	os.rename('hasmsg_validation.csv', 'second_hasmsg_validation.csv')
except:
	pass