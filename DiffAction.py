from lib.Constants import Constants
from lib.Output import Out
from lib.Utility import Utility

import TableDisplay


class Difference:
    def __init__(self, propertyName, errorCodeName, firstValue, secondValue):
        self.PropertyName = propertyName
        self.ErrorCodeName = errorCodeName
        self.FirstValue = firstValue
        self.SecondValue = secondValue

class ErrorCodeDifference:
    def __init__(self, errorCodeLeft, errorCodeRight):
        self.ErrorCodeLeft = errorCodeLeft
        self.ErrorCodeRight = errorCodeRight

def CompareLists(firstList, secondList):
    comparison = list()

    for first in firstList:
        found = False
        for second in secondList:
            if(first.ErrorName == second.ErrorName):
                found = True
                break
        if(found == False):
            comparison.append(first.ErrorName)

    return comparison

def ActionDiffErrorCodes(errorLists, errorSources):
    tiedResults = (CompareLists(*errorLists[0]), CompareLists(*errorLists[1]))
    # Untie method is packed in last argument of packed argument
    untieSources = errorSources[-1]
    firstSource, secondSource = untieSources()

    differenceListing = list()
    outerIndex = 0
    while(outerIndex < len(tiedResults[0])):
        if(outerIndex < len(tiedResults[1])):
            differenceListing.append(ErrorCodeDifference(tiedResults[0][outerIndex], tiedResults[1][outerIndex]))
        else:
            differenceListing.append(ErrorCodeDifference(tiedResults[0][outerIndex], ''))
        outerIndex += 1

    while(outerIndex < len(tiedResults[1])):
        differenceListing.append(ErrorCodeDifference('', tiedResults[1][outerIndex]))
        outerIndex += 1

    return differenceListing
    

def ActionDiffOnErrorLists(firstSet, secondSet, whatToDiff, showAll=False):
    if('Diff-Types' == whatToDiff or 'Diff-All' == whatToDiff):
        differenceListing = list()
        differenceCount = 0
        for first in firstSet:
            for second in secondSet:
                if(second.ErrorName == first.ErrorName):
                    if(showAll or second.ErrorType != first.ErrorType):
                        differenceListing.append(Difference(Constants.ErrorTypeProperty, first.ErrorName, first.ErrorType, second.ErrorType))
                        if(second.ErrorType != first.ErrorType):
                            differenceCount += 1

        return differenceListing

    if('Diff-Msgs' in whatToDiff or 'Diff-All' in whatToDiff):
        differenceListing = []

        for first in firstSet:
            for second in secondSet:
                if(second.ErrorName == first.ErrorName):
                    firstDisplayMsg = first.ErrorDisplayMsg.translate(str.maketrans('','',' \t\r\n'))
                    firstDisplayMsg = firstDisplayMsg.replace(chr(183),"")
                    firstDisplayMsg = firstDisplayMsg.replace(chr(8226),"")
                    secondDisplayMsg = second.ErrorDisplayMsg.translate(str.maketrans('','',' \t\r\n'))
                    secondDisplayMsg = secondDisplayMsg.replace(chr(183),"")
                    secondDisplayMsg = secondDisplayMsg.replace(chr(8226),"")
                    if(firstDisplayMsg != secondDisplayMsg):
                        differenceListing.append(Difference(Constants.ErrorDisplayMsgProperty, first.ErrorName, firstDisplayMsg, secondDisplayMsg))
        return differenceListing

    