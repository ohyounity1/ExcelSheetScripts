from dataclasses import dataclass
from pathlib import Path

from . import ValidationClasses
from . import DiffClasses

from ..ErrorCodes import ErrorCode

@dataclass
class JoinData:
    ErrorCode_1 : str
    ErrorCode_2 : str
    ErrorType_1 : ErrorCode.ErrorType
    ErrorType_2 : ErrorCode.ErrorType
    ErrorModule : str
    ErrorModuleSuggestions: [str]
    ErrorHasMsg_1 : bool
    ErrorHasMsgSuggestion_1: bool
    ErrorMsg_1 : str
    ErrorHasMsg_2 : bool
    ErrorHasMsgSuggestion_2: bool
    ErrorMsg_2 : str

class JoinAnalyzer:
    def __init__(self, mainSourceFile, secondarySourceFile, differ, arguments):
        self.MainSourceFile = mainSourceFile
        self.SecondarySourceFile = secondarySourceFile
        self.Differ = differ
        self.Arguments = arguments
    def __call__(self, sourceTuples):

        totalJoinData = []
        for sourceTuple in sourceTuples:
            errorSourceOne = sourceTuple[0]
            errorSourceTwo = sourceTuple[1]
            moduleSuggestions = []
            module = ''
            if(Path(self.MainSourceFile).suffix == '.json' and errorSourceOne is not None):
                moduleSuggestions = ValidationClasses.ModuleTypesValidator.ModuleSuggestionAlgorithm(errorSourceOne.ErrorName)
                module = errorSourceOne.ErrorModule
            elif(Path(self.SecondarySourceFile).suffix == '.json' and errorSourceTwo is not None):
                moduleSuggestions = ValidationClasses.ModuleTypesValidator.ModuleSuggestionAlgorithm(errorSourceTwo.ErrorName)
                module = errorSourceTwo.ErrorModule

            mismatchOne = False
            if(errorSourceOne is not None):
                mismatchOne = ValidationClasses.HasMsgValidator.HasMsgAlgorithm(errorSourceOne)
            mismatchTwo = False

            if(errorSourceTwo is not None):
                mismatchTwo = ValidationClasses.HasMsgValidator.HasMsgAlgorithm(errorSourceTwo)

            if(errorSourceOne is not None and errorSourceTwo is not None):
                totalJoinData.append(JoinData(errorSourceOne.ErrorName, errorSourceTwo.ErrorName,
                    errorSourceOne.ErrorType, errorSourceTwo.ErrorType,
                    module, moduleSuggestions, 
                    errorSourceOne.ErrorDisplaysMsg, len(errorSourceOne.ErrorDisplayMsg) > 0, errorSourceOne.ErrorDisplayMsg,
                    errorSourceTwo.ErrorDisplaysMsg, len(errorSourceTwo.ErrorDisplayMsg) > 0, errorSourceTwo.ErrorDisplayMsg))
            elif(errorSourceOne is None and errorSourceTwo is not None):
                totalJoinData.append(JoinData('', errorSourceTwo.ErrorName,
                    ErrorCode.ErrorType.Unknown(), errorSourceTwo.ErrorType,
                    module, moduleSuggestions, 
                    False, False, '',
                    errorSourceTwo.ErrorDisplaysMsg, len(errorSourceTwo.ErrorDisplayMsg) > 0, errorSourceTwo.ErrorDisplayMsg))
            elif(errorSourceOne is not None and errorSourceTwo is None):
                totalJoinData.append(JoinData(errorSourceOne.ErrorName, '',
                    errorSourceOne.ErrorType, ErrorCode.ErrorType.Unknown(),
                    module, moduleSuggestions, 
                    errorSourceOne.ErrorDisplaysMsg, len(errorSourceOne.ErrorDisplayMsg) > 0, errorSourceOne.ErrorDisplayMsg,
                    False, False, ''))

        self.Differ.Write('TOTAL JOIN TABLE SUMMARY:::::')
        self.Differ.Write(f'\n\tFirstValueSource = {self.MainSourceFile}\n\tSecondValueSource = {self.SecondarySourceFile}')
        self.Differ.Diff(totalJoinData, ['ErrorCode_1', 'ErrorCode_2', 
            'ErrorType_1', 'ErrorType_2',
            'ErrorModule', 'ErrorModuleSuggestions', 
            'ErrorHasMsg_1', 'ErrorHasMsgSuggestion_1', 'ErrorMsg_1',
            'ErrorHasMsg_2', 'ErrorHasMsgSuggestion_2', 'ErrorMsg_2'])

    def CsvFormatter(name, data):
        if(name == 'ErrorType_1' or name == 'ErrorType_2'):
            if(data == ErrorCode.ErrorType.UNKNOWN):
                return ''
            return str(data)
        elif(name == 'ErrorModuleSuggestions'):
            joined = ','.join(data)
            return f'"{joined}"'
        elif(name == 'ErrorHasMsg_1' or name == 'ErrorHasMsg_2' or name == 'ErrorHasMsgSuggestion_1' or name == 'ErrorHasMsgSuggestion_2'):
            return str(data)
        elif(name == 'ErrorMsg_1' or name == 'ErrorMsg_2'):
            if(len(data) > 0):
                data = data.replace('"', '""')
                return f'"{data}"'

        return data

def JoinAnalyzerFactory(mainSourceFile, secondarySourceFile, arguments):
    differ = None
    if(arguments.Export == 'csv'):
        differ = DiffClasses.CsvDiff('table_join', JoinAnalyzer.CsvFormatter)

    if(differ is None):
        raise Exception()

    return JoinAnalyzer(mainSourceFile, secondarySourceFile, differ, arguments)
