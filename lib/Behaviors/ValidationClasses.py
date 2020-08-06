from dataclasses import dataclass
from pathlib import Path

from . import DiffAnalyzers
from . import DiffClasses
from . import BehaviorConverters

from lib.Output import Out

@dataclass
class ModuleValidation:
    ErrorCodeName: str
    CurrentModule: str
    SuggestedModules: [str]

class ValidationAnalyzer:
    def __init__(self, sourceFile, differ, arguments):
        self.SourceFile = sourceFile
        self.Differ = differ
        self.Arguments = arguments

    def __RUN_ANALYZER__(self, source, showAll):
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

    def __call__(self, source):
        Out.VerbosePrint(Out.Verbosity.MEDIUM, 'ValidationAnalyzer: __call__')
        diffs, count = self.__RUN_ANALYZER__([x for x in source if x is not None], self.Arguments.DiffShowAll)
        msgHeaders = self.__MSG_HEADERS__(count)
        self.__DIFF_DISPLAY__(diffs, msgHeaders)

class ModuleTypesValidator(ValidationAnalyzer):
    def ModuleSuggestionAlgorithm(errorCode):
        def ANY(s, x):
            return len([item for item in x if item in s]) > 0

        def ALL(s, x):
            return len([item for item in x if item in s]) == len(x)

        modulesFoundInName = {
            'InboxSlot': lambda s: ALL(s, ['ENTRY', 'HOTEL']) and ANY(s, ['SLOT1', 'SLOT2', 'SLOT3', 'SLOT4', 'SLOT5']),
            'OutboxSlot': lambda s: ALL(s, ['EXIT', 'HOTEL']) and ANY(s, ['SLOT1', 'SLOT2', 'SLOT3', 'SLOT4', 'SLOT5']),
            'RfidProbesOil1': lambda s: ALL(s, ['RFID', 'P1']),
            'RfidProbesOil2': lambda s: ALL(s, ['RFID', 'P2']),
            'RfidEvagreenOil1': lambda s: ALL(s, ['RFID', 'E1']),
            'RfidEvagreenOil2': lambda s: ALL(s, ['RFID', 'E2']),
            'RfidWaste1': lambda s: ALL(s, ['RFID', 'W1']),
            'RfidWaste2': lambda s: ALL(s, ['RFID', 'W2']),
            'RfidDrOil1': lambda s: ALL(s, ['RFID', 'D1']),
            'RfidDrOil2': lambda s: ALL(s, ['RFID', 'D2']),
            'BottleAndFanController': lambda s: 'BFC' in s or ALL(s, ['BOTTLE', 'AND', 'FAN', 'CONTROLLER']),
            'FrontDoorRfid': lambda s: ALL(s, ['FRONT', 'DOOR', 'RFID']) or 'FrontDoorRfid' in s,
            'Inbox': lambda s: ALL(s, ['ENTRY', 'HOTEL']),
            'Outbox': lambda s: ALL(s, ['EXIT', 'HOTEL']),
            'FrontDoor': lambda s: ALL(s, ['FRONT', 'DOOR']),
            'Slot': lambda s: ANY(s, ['SLOT1', 'SLOT2', 'SLOT3', 'SLOT4', 'SLOT5']) or ANY(s, ['Slot1', 'Slot2', 'Slot3', 'Slot4', 'Slot5']),
            'PlateHandler': lambda s: 'HANDLER' in s or 'PlateHandler' in s or 'PH' in s,
            'DG': lambda s: 'DG' in s,
            'DR': lambda s: 'DR' in s and 'DROPLET_GENERATION' not in s,
            'TC': lambda s: 'TC' in s and 'CATCH' not in s,
            'Instrument': lambda s: 'CONTROLLER' in s,
            'Bottles': lambda s: 'BOTTLE' in s or ALL(s, ['INSUFFICIENT', 'OIL']) or ALL(s, ['INSUFFICIENT', 'WASTE']),
            'InboxDoor': lambda s: 'InboxDoor' in s,
            'OutboxDoor': lambda s: 'OutboxDoor' in s,
        }

        errorCodeNameSplit = errorCode.split('_')

        suggestionsForThisCode = []
        for moduleName in modulesFoundInName:
            if(modulesFoundInName[moduleName](errorCodeNameSplit)):
                suggestionsForThisCode.append(moduleName)

        if(len(suggestionsForThisCode) == 0):
            Out.VerbosePrint(Out.Verbosity.LOW, f'{errorCode} had no found module suggestions... adding instrument to suggestion list as fallback')
            suggestionsForThisCode.append('Instrument')

        return suggestionsForThisCode

    def __RUN_ANALYZER__(self, source, showAll):
        Out.VerbosePrint(Out.Verbosity.MEDIUM, 'ModuleTypesValidator: __RUN_ANALYZER__')
        suggestions = []
        actualCount = 0

        if(Path(self.SourceFile).suffix != '.json'):
            Out.VerbosePrint(Out.Verbosity.LOW, f'Skipping module analysis on {self.SourceFile} since it has no modules')
            return suggestions, actualCount

        Out.VerbosePrint(Out.Verbosity.LOW, f'Running module analysis on {self.SourceFile} for {len(source)} items...')

        for ec in source:
            errorCodeName = ec.ErrorName
            errorCodeModule = ec.ErrorModule

            errorCodeNameSplit = errorCodeName.split('_')

            suggestionsForThisCode = ModuleTypesValidator.ModuleSuggestionAlgorithm(errorCodeName)

            if(errorCodeModule in suggestionsForThisCode):
                Out.VerbosePrint(Out.Verbosity.HIGH, f'{errorCodeName}: Good matching module type found {errorCodeModule}')
            else:
                separator = ','
                actualCount += 1
                Out.VerbosePrint(Out.Verbosity.MEDIUM, f'{errorCodeName}:  Current module name {errorCodeModule} not a good match... suggestions are: {separator.join(suggestionsForThisCode)}')

            if(self.Arguments.DiffShowAll or errorCodeModule not in suggestionsForThisCode):
                suggestions.append(ModuleValidation(errorCodeName, errorCodeModule, suggestionsForThisCode))

        return suggestions, actualCount

    def __MSG_HEADERS__(self, count):
        return ['MODULE SUGGESTIONS SUMMARY:::::',
            f'\n\tTotal Possible Wrong Module Assignments = {count} from {self.SourceFile}']

    def __PROPERTIES__(self):
        return ['ErrorCodeName', 'CurrentModule', 'SuggestedModules']

@dataclass
class HasMsgValidation:
    ErrorCodeName: str
    HasMsgValue: bool
    SuggestedValue: bool
    Message: str = ""

class HasMsgValidator(ValidationAnalyzer):
    def HasMsgAlgorithm(ec):
        errorCodeName = ec.ErrorName
        hasMsg = ec.ErrorDisplaysMsg
        msg = ec.ErrorDisplayMsg

        mismatch = False
        if(hasMsg and len(msg) == 0):
            mismatch = True
            Out.VerbosePrint(Out.Verbosity.MEDIUM, f'{errorCodeName}:   Code configured with msg, but the message is empty!')
        elif(hasMsg == False and len(msg) > 0):
            mismatch = True
            Out.VerbosePrint(Out.Verbosity.MEDIUM, f'{errorCodeName}:   Code configured with no msg, but the message is {msg}!')

        return mismatch
    def __RUN_ANALYZER__(self, source, showAll):
        validations = []
        actualCount = 0

        for ec in source:
            errorCodeName = ec.ErrorName
            hasMsg = ec.ErrorDisplaysMsg
            msg = ec.ErrorDisplayMsg

            mismatch = HasMsgValidator.HasMsgAlgorithm(ec)

            if(self.Arguments.DiffShowAll or mismatch):
                validations.append(HasMsgValidation(errorCodeName, hasMsg, hasMsg == False, msg))

            if(mismatch):
                actualCount += 1
        return validations, actualCount

    def __MSG_HEADERS__(self, count):
        return ['HAS MESSAGE SUMMARY:::::',
            f'\n\tTotal Possible Wrong Message Configurations = {count} from {self.SourceFile}']

    def __PROPERTIES__(self):
        return ['ErrorCodeName', 'HasMsgValue', 'SuggestedValue', 'Message']

def MakeTableDiff(action, suffix):
    if(action == 'modules'):
        return DiffClasses.TableDiff(BehaviorConverters.StandardBehaviorConverters.TableModuleValidationDataConverter)
    elif(action == 'hasmsg'):
        return DiffClasses.TableDiff(BehaviorConverters.StandardBehaviorConverters.TableModuleHasMsgValidationDataConverter)

    raise Exception(f'Unhandled action type {action}')

def MakeCsvDiff(action, suffix):
    fileName = action + suffix
    if(action == 'modules'):
        return DiffClasses.CsvDiff(fileName, BehaviorConverters.StandardBehaviorConverters.CsvModuleValidationDataConverter)
    elif(action == 'hasmsg'):
        return DiffClasses.CsvDiff(fileName, BehaviorConverters.StandardBehaviorConverters.CsvModuleHasMsgValidationDataConverter)

    raise Exception(f'Unhandled action type {action}')

DiffValidationFactory = DiffClasses.DifferFactoryDecor(MakeTableDiff, MakeCsvDiff)

def ValidatorFactory(sourceFile, arguments, action, instance=1):
    differ = DiffValidationFactory(arguments, action, f'_validation_{instance}')
    if(action == 'modules'):
        return ModuleTypesValidator(sourceFile, differ, arguments)
    elif(action == 'hasmsg'):
        return HasMsgValidator(sourceFile, differ, arguments)
