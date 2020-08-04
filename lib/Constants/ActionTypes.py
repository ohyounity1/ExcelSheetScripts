class DiffActions:
    CODES = 'codes'
    TYPES = 'types'
    MSGS = 'msgs'
    def Values():
    	return [DiffActions.CODES, DiffActions.TYPES, DiffActions.MSGS]
    def Iter():
    	yield DiffActions.CODES
    	yield DiffActions.TYPES
    	yield DiffActions.MSGS