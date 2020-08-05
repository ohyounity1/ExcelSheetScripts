import difflib

from lib.Output import Out
from lib.Output import TableDisplay
from lib.Output import CsvDisplay
from lib.Output import TreeDisplay

import Converters

class DiffClass:
    def Write(self, msg):
        pass
    def Diff(diffs, properties):
        pass

class CompositeDiffClass(DiffClass):
    def __init__(self, composed):
        self.Composed = composed
    def Write(self, msg):
        for c in self.Composed:
            c.Write(msg)
    def Diff(self, diffs, properties):
        for c in self.Composed:
            c.Diff(diffs, properties)

class SingleDiffClassBase(DiffClass):
    def __init__(self, formatter, output, converter=None):
        self.Formatter = formatter
        self.Output = output
        self.Converter = converter
    def Write(self, msg):
        msg = self.Formatter(msg)
        self.Output(msg)

class TableDiff(SingleDiffClassBase):
    def __init__(self, converter=None):
        def __FORMATTER__(msg):
            return msg
        super().__init__(__FORMATTER__, Out.RegularPrint, converter)
        self.Converter = converter
    def Diff(self, diffs, properties):
        TableDisplay.ErrorListToTableDisplay(diffs, properties, self.Converter)

class TreeDiff(SingleDiffClassBase):
    def __init__(self, converter=None):
        def __FORMATTER__(msg):
            return msg
        super().__init__(__FORMATTER__, Out.RegularPrint, converter)
        self.Converter = converter
    def __ConvertProperties__(self, properties):
        pass
    def Diff(self, diffs, properties):
        TreeDisplay.ErrorListToTreeDisplay(diffs, self.__ConvertProperties__(properties), self.Converter)

class CsvDiff(SingleDiffClassBase):
    def __init__(self, fileName, converter=None):
        def __FORMATTER__(msg):
            return f'\n{msg}'
        self.File = open(fileName + '.csv', 'w')
        super().__init__(__FORMATTER__, self.File.write, converter)
    def Diff(self, diffs, properties):
        CsvDisplay.ErrorListToCSVDisplay(self.File, diffs, properties, self.Converter)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback ):
        self.File.close()

class MsgTreeDiffDecorator(TreeDiff):
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

class MsgDiffDecorator(SingleDiffClassBase):
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
            translatedDiffs.append(MsgDiffDecorator.MsgDifference(diff.ErrorCodeName, reasonString, first, second))

        self.Decorator.Diff(translatedDiffs, ['ErrorCode', 'Reason', 'FirstValue', 'SecondValue'])

    def ConvertMsgDiffCsvFormat(name, data):
        if(len(data) > 0 and (name == 'Reason' or name == 'FirstValue' or name == 'SecondValue')):
            data = data.replace('"', '""')
            return f'"{data}"'    
        return data

def MakeTableDiff(action):
    tableDiff = TableDiff()
    if(action == 'types'):
        tableDiff = TableDiff(Converters.ConvertErrorTypeDiffDisplayMsg)
    elif(action == 'msgs'):
        tableDiff = MsgTreeDiffDecorator()
    return tableDiff

def MakeCsvDiff(action):
    csvDiff = CsvDiff(action + '_diff')
    if(action == 'types'):
        csvDiff = CsvDiff(action + '_diff', Converters.ConvertErrorTypeDiffDisplayMsg)
    elif(action == 'msgs'):
        csvDiff = CsvDiff(action + '_diff', MsgDiffDecorator.ConvertMsgDiffCsvFormat)
    return csvDiff

def DifferFactory(arguments, action):
    differ = None
    if(arguments.Destination != 'null' and arguments.Export == 'csv'):
        differ = CompositeDiffClass([MakeTableDiff(action), MakeCsvDiff(action)])
    elif(arguments.Export == 'csv'):
        differ = MakeCsvDiff(action)
    elif(arguments.Destination != 'null'):
        differ = MakeTableDiff(action)
    else:
        exit()

    if(action == 'msgs'):
        differ = MsgDiffDecorator(differ)
    return differ

def DifferFactoryDecor(outFactory, diffFactory):
    def __INTERNAL__(arguments, name):
        differ = None
        if(arguments.Destination != 'null' and arguments.Export == 'csv'):
            differ = CompositeDiffClass([outFactory(name), diffFactory(name)])
        elif(arguments.Export == 'csv'):
            differ = diffFactory(name)
        elif(arguments.Destination != 'null'):
            differ = outFactory(name)
        else:
            exit()

        return differ
    return __INTERNAL__
