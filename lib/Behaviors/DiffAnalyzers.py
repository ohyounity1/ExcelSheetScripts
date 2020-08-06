import difflib

from . import DiffClasses
from . import DiffAction

from lib.Utility import Utility
from lib.Utility import Debug

from lib.Output import Out
from lib.Output import TreeDisplay

class DifferenceAnalyzer:
    def __init__(self, mainSourceFile, secondarySourceFile, differ, arguments):
        self.MainSourceFile = mainSourceFile
        self.SecondarySourceFile = secondarySourceFile
        self.Differ = differ
        self.Arguments = arguments
    def __RUN_ANALYZER__(self, sourceTuple, showAll):
        pass
    def __MSG_HEADERS__(self, count):
        pass
    def __PROPERTIES__(self):
        pass
    def __DIFF_DISPLAY__(self, diffs, msgs):
        for msg in msgs:
            self.Differ.Write(msg)
        if(len(diffs) > 0):
            self.Differ.Diff(diffs, self.__PROPERTIES__())
    @Debug.DebugClassMethod
    def __call__(self, sourceTuples):
        diffs, count = self.__RUN_ANALYZER__(sourceTuples, self.Arguments.DiffShowAll)
        msgHeaders = self.__MSG_HEADERS__(count)
        self.__DIFF_DISPLAY__(diffs, msgHeaders)

class CodesDifferenceAnalyzer(DifferenceAnalyzer):
    @Debug.DebugClassMethod
    def __RUN_ANALYZER__(self, sourceTuple, showAll):
        return DiffAction.ActionDiffErrorCodes(sourceTuple, showAll)
    @Debug.DebugClassMethod
    def __PROPERTIES__(self):
        return ['FirstValue', 'SecondValue']
    @Debug.DebugClassMethod
    def __MSG_HEADERS__(self, count):
        return ['ERROR CODE SUMMARY:::::',
            f'\n\tFirstValueSource = \n\t\tErrors in {self.MainSourceFile}, but not in {self.SecondarySourceFile}\n\tSecondValueSource = \n\t\tErrors in {self.SecondarySourceFile}, but not in {self.MainSourceFile}\n\tTotalDifferences = {count}']
         
class TypesDifferenceAnalyzer(DifferenceAnalyzer):
    def __RUN_ANALYZER__(self, sourceTuple, showAll):
        return DiffAction.ActionDiffTypesOnErrorLists(sourceTuple, showAll)
    def __PROPERTIES__(self):
        return ['ErrorCodeName', 'FirstValue', 'SecondValue']
    def __MSG_HEADERS__(self, count):
        return [f'FirstValue = {self.MainSourceFile}\nSecondValue = {self.SecondarySourceFile}\nTotalDifferences = {count}']
    def ConvertErrorTypeDiffDisplayMsg(name, data):
        if(name == 'FirstValue' or name == 'SecondValue'):
            return str(data)
        return data

class MsgsDifferenceAnalyzer(DifferenceAnalyzer):
    def __RUN_ANALYZER__(self, sourceTuple, showAll):
        return DiffAction.ActionDiffMsgsOnErrorLists(sourceTuple, showAll)
    def __PROPERTIES__(self):
        return []
    def __MSG_HEADERS__(self, count):
        return [f'FirstValue = {self.MainSourceFile}\nSecondValue = {self.SecondarySourceFile}\nTotalDifferences = {count}']


class MsgTreeDiffDecorator(DiffClasses.TreeDiff):
    def __init__(self, converter=None):
        super().__init__(converter)
    def __ConvertProperties__(self, properties):

        __properties = list()
        __properties.append(TreeDisplay.TreeProperty(Name='FirstValue', ValueOnNextLevel=True))
        __properties.append(TreeDisplay.TreeProperty(Name='SecondValue', ValueOnNextLevel=True))

        _properties = list()
        _properties.append(TreeDisplay.TreeProperty(Name='Reason', Children=__properties[:]))

        localProperties = list()
        localProperties.append(TreeDisplay.TreeProperty(Name='ErrorCode', Children=_properties[:]))
        return localProperties

class MsgDiffDecorator(DiffClasses.SingleDiffClassBase):
    from dataclasses import dataclass

    @dataclass
    class MsgDifference:
        ErrorCode: str
        Reason: str
        FirstValue: str
        SecondValue : str

    def __init__(self, decorator, converter=None):
        def __FORMATTER__(msg):
            pass
        def __OUTPUT__ (msg):
            pass
        super().__init__(__FORMATTER__, __OUTPUT__, converter)
        self.Decorator = decorator
    def Write(self, msg):
        self.Decorator.Write(msg)
    def Diff(self, diffs, properties):
        translatedDiffs = []
        for diff in diffs:
            first = diff.FirstValue
            second = diff.SecondValue
            reasonString = 'Matches!  In ShowAll Mode'
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
            translatedDiffs.append(MsgDiffDecorator.MsgDifference(diff.ErrorCodeName, reasonString, first, second))

        self.Decorator.Diff(translatedDiffs, ['ErrorCode', 'Reason', 'FirstValue', 'SecondValue'])

    def ConvertMsgDiffCsvFormat(name, data):
        if(len(data) > 0 and (name == 'Reason' or name == 'FirstValue' or name == 'SecondValue')):
            data = data.replace('"', '""')
            return f'"{data}"'    
        return data

def MakeTableDiff(action, suffix):
    if(action == 'types'):
        return DiffClasses.TableDiff(TypesDifferenceAnalyzer.ConvertErrorTypeDiffDisplayMsg)
    elif(action == 'codes'):
        return DiffClasses.TableDiff()
    elif(action == 'msgs'):
        return MsgTreeDiffDecorator()
    raise Exception(f'Unhandled action type {action}')

def MakeCsvDiff(action, suffix):
    fileName = action + suffix
    if(action == 'types'):
        return DiffClasses.CsvDiff(fileName, TypesDifferenceAnalyzer.ConvertErrorTypeDiffDisplayMsg)
    elif(action == 'codes'):
        return DiffClasses.CsvDiff(fileName)
    elif(action == 'msgs'):
        return DiffClasses.CsvDiff(fileName, MsgDiffDecorator.ConvertMsgDiffCsvFormat)
    raise Exception(f'Unhandled action type {action}')

DiffAnalyzerFactory = DiffClasses.DifferFactoryDecor(MakeTableDiff, MakeCsvDiff)

def AnalyzerFactory(mainSourceFile, secondarySourceFile, arguments, action):
    differ = DiffAnalyzerFactory(arguments, action, '_diff')
    if(action == 'codes'):
        return CodesDifferenceAnalyzer(mainSourceFile, secondarySourceFile, differ, arguments)
    elif(action == 'types'):
        return TypesDifferenceAnalyzer(mainSourceFile, secondarySourceFile, differ, arguments)
    elif(action == 'msgs'):
        finalDiffer = MsgDiffDecorator(differ)
        return MsgsDifferenceAnalyzer(mainSourceFile, secondarySourceFile, finalDiffer, arguments)

    raise Exception(f'Unhandled action type {action}')
