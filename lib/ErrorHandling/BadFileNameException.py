class BadFileNameException(Exception):
	def __init__(self, extension):
		self.Message = 'Invalid extension for this file {extension}'
	def __str__(self):
		return self.Message