from ..Output import Out
from ..Output import TableDisplay
from ..Output import CsvDisplay
from ..Output import TreeDisplay

from . import BehaviorConverters

class DiffClass:
    def Write(self, msg):
        pass
    def Diff(diffs, properties):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_Value, exc_Trace):
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
    def __exit__(self, exc_type, exc_Value, exc_Trace):
        for c in self.Composed:
            c.__exit__(exc_type, exc_Value, exc_Trace)

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


def DifferFactoryDecor(outFactory, exportFactory):
    def __INTERNAL__(arguments, name, suffix):
        differ = None
        if(arguments.Destination != 'null' and arguments.Export == 'csv'):
            differ = CompositeDiffClass([outFactory(name, suffix), exportFactory(name, suffix)])
        elif(arguments.Export == 'csv'):
            differ = exportFactory(name, suffix)
        elif(arguments.Destination != 'null'):
            differ = outFactory(name, suffix)
        else:
            raise Exception()

        return differ
    return __INTERNAL__
