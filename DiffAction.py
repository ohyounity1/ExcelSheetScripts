
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