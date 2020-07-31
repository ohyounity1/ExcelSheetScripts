import sys

from enum import IntEnum
from functools import total_ordering

from ..Constants import Colours

__VERBOSITY__ = None

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

def SetVerbosity(verbosity):
	global __VERBOSITY__
	if(__VERBOSITY__ is None):
		__VERBOSITY__ = Verbosity(verbosity)
    
def ErrorPrinter(method):
    def __ErrorPrinter__(output):
        # Wrap around fail text first
        method(Colours.Colours.FailText(output))
        # Now close application
        exit()
    # Return the decorator
    return __ErrorPrinter__

#Default to basic output
ErrorPrint = ErrorPrinter(print)


def VerbosePrinter(printer):
	def __VerbosePrinter__(level, output):
		global __VERBOSITY__
		if(level <= __VERBOSITY__):
			printer(output)
	return __VerbosePrinter__

# Default to basic output
VerbosePrint = VerbosePrinter(print)
