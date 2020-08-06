class DiffActions:
    CODES = 'codes'
    TYPES = 'types'
    MSGS = 'msgs'
    def Values():
    	return [DiffActions.CODES, DiffActions.TYPES, DiffActions.MSGS]

class ValidateActions:
	MODULES = 'modules'
	HASMSG = 'hasmsg'
	def Values():
		return [ValidateActions.MODULES, ValidateActions.HASMSG]
