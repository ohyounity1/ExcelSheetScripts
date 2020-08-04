class Destinations:
	Prompt = 'prompt'
	Null = 'null'
	File = 'file'

	def OutputFileName():
		return 'Output.Log'
	def Values():
		return [Destinations.Prompt, Destinations.Null, Destinations.File]

class Exports:
	CSV = 'csv'

	def Values():
		return [Exports.CSV]