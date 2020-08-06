import sys

from enum import IntEnum
from functools import total_ordering

from ..Constants import Colours
from ..Constants import Destinations

@total_ordering
class Verbosity(IntEnum):

	"""Summary
	
	Attributes:
	    HIGH (int): Description
	    LOW (int): Description
	    MEDIUM (int): Description
	    NONE (int): Description
	    Value (TYPE): Description
	"""
	
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
		"""Summary
		
		Args:
		    value (TYPE, optional): Description
		"""
		self.Value = value
	def __repr__(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		return self.__mapping__[self.Value]
	def __lt__(self, compare):
		"""Summary
		
		Args:
		    compare (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		return int(self.Value) < int(compare)
	def __eq__(self, compare):
		"""Summary
		
		Args:
		    compare (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		return int(self.Value) == int(self.Value)

class Logger:

	"""Summary
	
	Attributes:
	    Logger (TYPE): Description
	"""
	
	def __init__(self, file):
		"""Summary
		
		Args:
		    file (TYPE): Description
		"""
		self.Logger = open(file, 'w')
	def Write(self, msg):
		"""Summary
		
		Args:
		    msg (TYPE): Description
		"""
		self.Logger.write(f'\n{msg}')

def ErrorPrinter():
    """Summary
    
    Returns:
        TYPE: Description
    """
    def __ErrorPrinter__(output):
        """Summary
        
        Args:
            output (TYPE): Description
        """
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
	"""Summary
	
	Args:
	    index (TYPE): Description
	    method (TYPE): Description
	"""
	__OUT_PLUGINS__[index] = method

# Regular output goes to print
RegisterOutPlugin(Destinations.Destinations.Prompt, print)
# For null, do nothing
RegisterOutPlugin(Destinations.Destinations.Null, lambda *args: None)

def LogPrint(fileName):
	"""Summary
	
	Args:
	    fileName (TYPE): Description
	
	Returns:
	    TYPE: Description
	"""
	logger = Logger(fileName)
	def __LOGGER__(msg):
		"""Summary
		
		Args:
		    msg (TYPE): Description
		"""
		logger.Write(msg)
	return __LOGGER__

def PrintPlugin(index):
	"""Summary
	
	Args:
	    index (TYPE): Description
	
	Returns:
	    TYPE: Description
	"""
	printer = __OUT_PLUGINS__[index]
	def __PRINTER__(msg):
		"""Summary
		
		Args:
		    msg (TYPE): Description
		"""
		printer(msg)
	return __PRINTER__

def VerbosePrinter(setLevel, index):
	"""Summary
	
	Args:
	    setLevel (TYPE): Description
	    index (TYPE): Description
	
	Returns:
	    TYPE: Description
	"""
	printer = __OUT_PLUGINS__[index]
	def __VerbosePrinter__(level, output):
		"""Summary
		
		Args:
		    level (TYPE): Description
		    output (TYPE): Description
		"""
		if(level <= setLevel):
			printer(output)
	return __VerbosePrinter__

# Default to basic output (and no verbosity)
VerbosePrint = VerbosePrinter(0, Destinations.Destinations.Prompt)

def RegularPrinter(index):
	"""Summary
	
	Args:
	    index (TYPE): Description
	
	Returns:
	    TYPE: Description
	"""
	printer = __OUT_PLUGINS__[index]
	def __RegularPrinter__(output):
		"""Summary
		
		Args:
		    output (TYPE): Description
		"""
		printer(output)
	return __RegularPrinter__

#Default main output to print
RegularPrint = RegularPrinter(Destinations.Destinations.Prompt)
