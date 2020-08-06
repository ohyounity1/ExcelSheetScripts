class Destinations:

	"""Class defining all destinations for script output
	
	Attributes:
	    File (str): Argument for directing to a file
	    Null (str): Argument for no output
	    Prompt (str): Argument for directing to the screen
	"""
	
	Prompt: str = 'prompt'
	Null: str = 'null'
	File: str = 'file'

	def FileName() -> str:
		"""Returns the name of the standard redirected output file
		
		Returns:
		    TYPE: Location of redirected output file
		"""
		return 'Output.Log'
	def Values() -> [str]:
		"""Returns list of all the possible properties
		
		Returns:
		    TYPE: List of all the types
		"""
		return [Destinations.Prompt, Destinations.Null, Destinations.File]

class Exports:

	"""Class defining all exports for script output
	
	Attributes:
	    CSV (str): Export to CSV
	"""
	
	CSV: str = 'csv'

	def CsvExportName(action) -> str:
		return f'{action}_export.csv'
	def Values() -> [str]:
		"""All possible export values
		
		Returns:
		    TYPE: All possible export values
		"""
		return [Exports.CSV]