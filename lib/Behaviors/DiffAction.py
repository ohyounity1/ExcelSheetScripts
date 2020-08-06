from dataclasses import dataclass

@dataclass
class Difference:
	ErrorCodeName: str
	FirstValue: str
	SecondValue: str

def RowCheckHelperMethod(row1, row2, provider, comparer, showAll):
	def __0__(differenceListing, counter):
		if(showAll):
			differenceListing.append(Difference(row2.ErrorName, '', provider(row2)))
	def __1__(differenceListing, counter):
		if(showAll):
			differenceListing.append(Difference(row1.ErrorName, provider(row1), ''))
	def __2__(differenceListing, counter):
		if(showAll):
			differenceListing.append(Difference('', '', ''))
	def __3__(differenceListing, counter):
		compared = comparer(row1, row2)
		if(showAll or compared):
			currentCount = counter[0]
			differenceListing.append(Difference(row1.ErrorName, provider(row1), provider(row2)))
			if(compared):
				counter[0] = currentCount + 1

	if(row1 is None and row2 is not None):
		return __0__
	elif(row1 is not None and row2 is None):
		return __1__
	elif(row1 is None and row2 is None):
		return __2__
	else:
		return __3__

def ActionDiffErrorCodes(sourceTuples, showAll=False):
	differenceListing = list()
	actualCount = 0
	for tuple in sourceTuples:
		# Item on left side of table is empty, but item on right isn't this was a bad join 
		# Leave item on left blank
		if(tuple[0] is None and tuple[1] is not None):
			differenceListing.append(Difference(tuple[1].ErrorName, '', tuple[1].ErrorName))
			actualCount += 1
		elif(tuple[0] is not None and tuple[1] is None):
			differenceListing.append(Difference(tuple[0].ErrorName, tuple[0].ErrorName, ''))
			actualCount += 1
		elif(showAll):
			if(tuple[0] is None and tuple[1] is None):
				differenceListing.append(Difference('', '', ''))
			else:
				differenceListing.append(Difference(tuple[0].ErrorName, tuple[0].ErrorName,tuple[0].ErrorName))
	return differenceListing, actualCount

def ActionDiffTypesOnErrorLists(sourceTuples, showAll=False):
	differenceListing = list()
	actualCount = 0

	actualCounterReference = [actualCount]
	for tuple in sourceTuples:
		RowCheckHelperMethod(tuple[0], tuple[1], lambda e: e.ErrorType, lambda e1, e2: e1.ErrorType != e2.ErrorType, showAll)(differenceListing, actualCounterReference)

	return differenceListing, actualCounterReference[0]

def ActionDiffMsgsOnErrorLists(sourceTuples, showAll=False):
	def __STRIP_CHARS__(msg):
		msg = msg.translate(str.maketrans('','',' \t\r\n'))
		msg = msg.replace(chr(183),"")
		msg = msg.replace(chr(8226),"")

		return msg
	differenceListing = []
	actualCount = 0
	actualCounterReference = [actualCount]

	for tuple in sourceTuples:
		RowCheckHelperMethod(tuple[0], tuple[1], lambda e: __STRIP_CHARS__(e.ErrorDisplayMsg), lambda e1, e2: __STRIP_CHARS__(e1.ErrorDisplayMsg) != __STRIP_CHARS__(e2.ErrorDisplayMsg), showAll)(differenceListing, actualCounterReference)

	return (differenceListing, actualCounterReference[0])

	