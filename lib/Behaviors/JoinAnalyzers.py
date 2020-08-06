class JoinAnalyzer:
    def __init__(self, mainSourceFile, secondarySourceFile, chain, arguments):
        self.MainSourceFile = mainSourceFile
        self.SecondarySourceFile = secondarySourceFile
        self.Arguments = arguments
    def __call__(self, mainSource, secondarySource):
        mainOrder = []
        secondaryOrder = []

        for errorCodeOne in mainSource:
            errorCodeName = errorCodeOne.ErrorName
            foundErrorCodeInSecondList = False
            for errorCodeTwo in secondarySource:
                if(errorCodeName == errorCodeTwo.ErrorName):
                    mainOrder.append(errorCodeOne)
                    secondOrder.append(errorCodeTwo)
                    foundErrorCodeInSecondList = True
                    break
            if(foundErrorCodeInSecondList == False):
                differenceCount += 1
                mainOrder.append(errorCodeOne)

        for errorCodeOne in secondarySource:
            errorCodeName = errorCodeOne.ErrorName
            foundErrorCodeInSecondList = False
            for errorCodeTwo in mainSource:
                if(errorCodeName == errorCodeTwo.ErrorName):
                    foundErrorCodeInSecondList = True
                    break
            if(foundErrorCodeInSecondList == False):
                differenceCount += 1
                secondaryOrder.append(errorCodeOne)
                
        return differenceListing, differenceCount


class ChainJoinAnalyzer:
    def __init__(self, mainSourceFile, secondarySourceFile, chain, arguments):
        self.MainSourceFile = mainSourceFile
        self.SecondarySourceFile = secondarySourceFile
        self.Chain = chain
        self.Arguments = arguments
    def __RUN_ANALYZER__(self, mainSource, secondarySource, showAll):
        pass
    def __MSG_HEADERS__(self, count):
        pass
    def __PROPERTIES__(self):
        pass
    def __DIFF_DISPLAY__(self, diffs, msgs):
        for msg in msgs:
            self.Differ.Write(msg)
        self.Differ.Diff(diffs, self.__PROPERTIES__())

    def __call__(self, mainSource, secondarySource):
        diffs = self.__RUN_ANALYZER__(mainSource, secondarySource, self.Arguments.DiffShowAll)
        if(len(diffs) > 0 and self.Chain != None):
            return self.Chain(diffs, mainSource, secondarySource)
        return diffs

class ErrorCodesChainJoinAnalyzer(ChainJoinAnalyzer):
    def __RUN_ANALYZER__(self, mainSource, secondarySource, showAll):
        codesList, count = DiffAction.ActionDiffErrorCodes(Utility.Tie(mainSource, secondarySource), showAll)
        return codesList

class ErrorTypesChainJoinAnalyzer(ChainJoinAnalyzer):
    def __init__(self, mainSourceFile, secondarySourceFile, arguments, typesDiff, msgDff, moduleValidator, msgValidator):
        self.MainSourceFile = mainSourceFile
        self.SecondarySourceFile = secondarySourceFile
        self.Chain = chain
        self.Arguments = arguments
