from lib.Constants import Constants

import TableDisplay
import difflib

class Difference:
    def __init__(self, propertyName, errorCodeName, firstValue, secondValue):
        self.PropertyName = propertyName
        self.ErrorCodeName = errorCodeName
        self.FirstValue = firstValue
        self.SecondValue = secondValue

def CompareLists(firstList, secondList):
    errorsInFirstNotInSecond = []
    for first in firstList:
        foundInSecondList = False
        firstErrorName = first.ErrorName
        for second in secondList:
            if(second.ErrorName == firstErrorName):
                foundInSecondList = True
                break
        if(foundInSecondList == False):
            errorsInFirstNotInSecond.append(firstErrorName)
            
    return errorsInFirstNotInSecond

def DisplayComparisons(differences, firstSource, secondSource):
    if(len(differences) > 0):
        print('Errors found in {}, but not in {}'.format(firstSource, secondSource))
        for x in differences:
            print(x)
            
            
def ActionDiffOnErrorLists(firstErrorList, firstSourceFile, secondErrorList, secondSourceFile):
    errorsInFirstNotInSecond = CompareLists(firstErrorList, secondErrorList)           
    errorsInSecondNotInFirst = CompareLists(secondErrorList, firstErrorList)
            
    DisplayComparisons(errorsInFirstNotInSecond, firstSourceFile, secondSourceFile)
    DisplayComparisons(errorsInSecondNotInFirst, secondSourceFile, firstSourceFile)
    
    differenceListing = []
    
    for first in firstErrorList:
        for second in secondErrorList:
            if(second.ErrorName == first.ErrorName):
                if(second.ErrorType != first.ErrorType):
                    differenceListing.append(Difference(Constants.ErrorTypeProperty, first.ErrorName, first.ErrorType, second.ErrorType))

    if(len(differenceListing) > 0):
        print('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(firstSourceFile, secondSourceFile, len(differenceListing)))
        TableDisplay.ErrorListToTableDisplay(differenceListing, ['ErrorCodeName', 'FirstValue', 'SecondValue'])
        
    differenceListing = []
    
    for first in firstErrorList:
        for second in secondErrorList:
            if(second.ErrorName == first.ErrorName):
                firstDisplayMsg = first.ErrorDisplayMsg.translate(str.maketrans('','',' \t\r\n'))
                firstDisplayMsg = firstDisplayMsg.replace(chr(183),"")
                firstDisplayMsg = firstDisplayMsg.replace(chr(8226),"")
                secondDisplayMsg = second.ErrorDisplayMsg.translate(str.maketrans('','',' \t\r\n'))
                secondDisplayMsg = secondDisplayMsg.replace(chr(183),"")
                secondDisplayMsg = secondDisplayMsg.replace(chr(8226),"")
                if(firstDisplayMsg != secondDisplayMsg):
                    differenceListing.append(Difference(Constants.ErrorDisplayMsgProperty, first.ErrorName, firstDisplayMsg, secondDisplayMsg))

    if(len(differenceListing) > 0):
        print('FirstValue = {}\nSecondValue = {}\nTotalDifferences = {}'.format(firstSourceFile, secondSourceFile, len(differenceListing)))
        for x in differenceListing:
            first = x.FirstValue
            second = x.SecondValue
            reasonString = ''
            if(len(first) == 0):
                reasonString = 'First display msg is empty!'
            elif(len(second) == 0):
                reasonString = 'Second display msg is empty!'
            else:
                for i,s in enumerate(difflib.ndiff(first, second)):
                    if s[0]==' ': continue
                    elif s[0]=='-':
                        reasonString += (u' Delete "{}" from position {} '.format(s[-1],i))
                        if(i < len(first)):
                            first = first[:i] + '[' + first[i] + ']' + first[i+1:]
                        
                        if(i < len(second)):
                            second = second[:i] + '[' + second[i] + ']' + second[i+1:]
                        break
                    elif s[0]=='+':
                        reasonString += (u' Add "{}" to position {} '.format(s[-1],i))    
                        if(i < len(first)):
                            first = first[:i] + '[' + first[i] + ']' + first[i+1:]
                        
                        if(i < len(second)):
                            second = second[:i] + '[' + second[i] + ']' + second[i+1:]
                        break
            print('\n{}\n--Summary:{}\n----{}\n------{}\n----{}\n------{}\n'.format(x.ErrorCodeName, reasonString, firstSourceFile, first, secondSourceFile, second))
             
