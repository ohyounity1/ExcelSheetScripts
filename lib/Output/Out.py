import sys

from enum import IntEnum
from functools import total_ordering

from ..Constants import Colours
from ..Constants import Destinations

@total_ordering
class Verbosity(IntEnum):
	NONE = 0
	LOW = 1
	MEDIUM = 2
	HIGH = 3
	__mapping__ = {
		NONE: "None",
		LOW: "Low",
		MEDIUM: "Medium",
		HIGH: "High"
	}
	def __init__(self, value=NONE):
		self.Value = value
	def __repr__(self):
		return self.__mapping__[self.Value]
	def __lt__(self, compare):
		return int(self.Value) < int(compare)
	def __eq__(self, compare):
		return int(self.Value) == int(self.Value)

class Logger:
	def __init__(self, file):
		self.Logger = open(file, 'w')
	def Write(self, msg):
		self.Logger.write(f'\n{msg}')

# Error printing
def ErrorPrinter():
    def __ErrorPrinter__(output):
        # Wrap around fail text first
        print(Colours.Colours.FailText(output))
        # Now close application
        exit()
    # Return the decorator
    return __ErrorPrinter__

#Default to basic output
ErrorPrint = ErrorPrinter()

# Define the various out plugins for printing the program's output
__OUT_PLUGINS__ = {}

def RegisterOutPlugin(index, method):
	__OUT_PLUGINS__[index] = method

# Regular output goes to print
RegisterOutPlugin(Destinations.Destinations.Prompt, print)
# For null, do nothing
RegisterOutPlugin(Destinations.Destinations.Null, lambda *args: None)


def LogPrint(fileName):
	logger = Logger(fileName)
	def __LOGGER__(msg):
		logger.Write(msg)
	return __LOGGER__

def PrintPlugin(index):
	printer = __OUT_PLUGINS__[index]
	def __PRINTER__(msg):
		printer(msg)
	return __PRINTER__

def VerbosePrinter(setLevel, index):
	printer = __OUT_PLUGINS__[index]
	def __VerbosePrinter__(level, output):
		if(level <= setLevel):
			printer(output)
	return __VerbosePrinter__

# Default to basic output (and no verbosity)
VerbosePrint = VerbosePrinter(0, Destinations.Destinations.Prompt)

def RegularPrinter(index):
	printer = __OUT_PLUGINS__[index]
	def __RegularPrinter__(output):
		printer(output)
	return __RegularPrinter__

#Default main output to print
RegularPrint = RegularPrinter(Destinations.Destinations.Prompt)
