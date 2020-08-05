from dataclasses import dataclass
from pathlib import Path

import DiffAnalyzers
import DiffClasses
import Converters

from lib.Output import Out

@dataclass
class ModuleValidation:
    ErrorCodeName: str
    CurrentModule: str
    SuggestedModules: [str]

class ModuleTypesValidator(DiffAnalyzers.DifferenceAnalyzer):
    def __RUN_ANALYZER__(self, mainSource, secondarySource, action, showAll):
        validateList = []

        chosenSourceFile = None

        if(Path(self.MainSourceFile).suffix == '.json'):
            validateList = mainSource
            chosenSourceFile = self.MainSourceFile
        elif(Path(self.SecondarySourceFile).suffix == '.json'):
            validateList = secondarySource
            chosenSourceFile = self.SecondarySourceFile

        suggestions = []
        actualCount = 0

        for ec in validateList:
            errorCodeName = ec.ErrorName
            errorCodeModule = ec.ErrorModule

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

            errorCodeNameSplit = errorCodeName.split('_')

            suggestionsForThisCode = []
            for moduleName in modulesFoundInName:
                if(modulesFoundInName[moduleName](errorCodeNameSplit)):
                    suggestionsForThisCode.append(moduleName)

            if(len(suggestionsForThisCode) == 0):
                Out.VerbosePrint(Out.Verbosity.LOW, f'{errorCodeName} had no found module suggestions... adding instrument to suggestion list as fallback')
                suggestionsForThisCode.append('Instrument')

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
            f'\n\t\n\tTotalDifferences = {count}']


def MakeTableDiff(action):
    tableDiff = DiffClasses.TableDiff()
    if(action == 'modules'):
        tableDiff = DiffClasses.TableDiff(Converters.TableModuleValidationDataConverter)
    return tableDiff

def MakeCsvDiff(action):
    csvDiff = DiffClasses.CsvDiff(action + '_validation')
    if(action == 'modules'):
        csvDiff = DiffClasses.CsvDiff(action + '_validation', Converters.CsvModuleValidationDataConverter)
    return csvDiff            

DiffFactory = DiffClasses.DifferFactoryDecor(MakeTableDiff, MakeCsvDiff)

def ValidatorFactory(mainSourceFile, secondarySourceFile, arguments, action):
    __VALIDATOR_PROPERTIES__ = {
        'modules': ['ErrorCodeName', 'CurrentModule', 'SuggestedModules']
    }
    properties = __VALIDATOR_PROPERTIES__[action]
    differ = DiffFactory(arguments, action)
    if(action == 'modules'):
        return ModuleTypesValidator(mainSourceFile, secondarySourceFile, differ, properties, arguments, action)
