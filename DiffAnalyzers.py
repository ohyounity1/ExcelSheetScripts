import DiffClasses
import DiffAction

from lib.Utility import Utility
from lib.Output import Out

class DifferenceAnalyzer:
    def __init__(self, mainSourceFile, secondarySourceFile, differ, properties, arguments, action):
        self.MainSourceFile = mainSourceFile
        self.SecondarySourceFile = secondarySourceFile
        self.Differ = differ
        self.Properties = properties
        self.Arguments = arguments
        self.Action = action

    def __RUN_ANALYZER__(self, mainSource, secondarySource, action, showAll):
        pass
    def __MSG_HEADERS__(self, count):
        pass
    def __DIFF_DISPLAY__(self, diffs, msgs):
        for msg in msgs:
            self.Differ.Write(msg)
        self.Differ.Diff(diffs, self.Properties)

    def RunAnalysis(self, mainSource, secondarySource):
        diffs, count = self.__RUN_ANALYZER__(mainSource, secondarySource, self.Action, self.Arguments.DiffShowAll)
        if(len(diffs) > 0):
            msgHeaders = self.__MSG_HEADERS__(count)
            self.__DIFF_DISPLAY__(diffs, msgHeaders)

class CodesDifferenceAnalyzer(DifferenceAnalyzer):
    def __RUN_ANALYZER__(self, mainSource, secondarySource, action, showAll):
        return DiffAction.ActionDiffErrorCodes(Utility.Tie(mainSource, secondarySource))
    def __MSG_HEADERS__(self, count):
        return ['ERROR CODE SUMMARY:::::',
            f'\n\tFirstValueSource = \n\t\tErrors in {self.MainSourceFile}, but not in {self.SecondarySourceFile}\n\tSecondValueSource = \n\t\tErrors in {self.SecondarySourceFile}, but not in {self.MainSourceFile}\n\tTotalDifferences = {count}']
         
class TypesDifferenceAnalyzer(DifferenceAnalyzer):
    def __RUN_ANALYZER__(self, mainSource, secondarySource, action, showAll):
        return DiffAction.ActionDiffOnErrorLists(mainSource, secondarySource, action, showAll)
    def __MSG_HEADERS__(self, count):
        return [f'FirstValue = {self.MainSourceFile}\nSecondValue = {self.SecondarySourceFile}\nTotalDifferences = {count}']

class MsgsDifferenceAnalyzer(DifferenceAnalyzer):
    def __RUN_ANALYZER__(self, mainSource, secondarySource, action, showAll):
        return DiffAction.ActionDiffOnErrorLists(mainSource, secondarySource, action, showAll)
    def __MSG_HEADERS__(self, count):
        return [f'FirstValue = {self.MainSourceFile}\nSecondValue = {self.SecondarySourceFile}\nTotalDifferences = {count}']

def AnalyzerFactory(mainSourceFile, secondarySourceFile, arguments, action):
    __ANALYZER_PROPERTIES__ = {
        'codes': ['FirstValue', 'SecondValue'],
        'types': ['ErrorCodeName', 'FirstValue', 'SecondValue'],
        'msgs': []
    }
    properties = __ANALYZER_PROPERTIES__[action]
    differ = DiffClasses.DifferFactory(arguments, action)
    if(action == 'codes'):
        return CodesDifferenceAnalyzer(mainSourceFile, secondarySourceFile, differ, properties, arguments, action)
    elif(action == 'types'):
        return TypesDifferenceAnalyzer(mainSourceFile, secondarySourceFile, differ, properties, arguments, action)
    elif(action == 'msgs'):
        return MsgsDifferenceAnalyzer(mainSourceFile, secondarySourceFile, differ, properties, arguments, action)
