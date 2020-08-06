from dataclasses import dataclass
from typing import Any

from .ErrorCodeHandler import ErrorCodeHandler
from .ErrorCodeHandler import ErrorCodeFilter

from ..ErrorCodes import ErrorCode

@dataclass
class SourceCenter:
    SourceName: str
    SourceResults: [ErrorCode.ErrorCode]

@dataclass
class SourceStrategy:
    PrintHeader: Any
    HandleErrorCode: Any
    ConvertData: Any

class ExportSources:
    def __init__(self):
        self.ExportFiles = list()
    def __add__(self, file):
        self.ExportFiles.append(file)
    def __iadd__(self, file):
        self.ExportFiles.append(file)        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_stacktrace):
        [f.close() for f in self.ExportFiles]

class SourceStrategyComposite:
    def __init__(self, strategies):
        self.Strategies = strategies
    @ErrorCodeFilter
    @ErrorCodeHandler
    def __call__(self, sourceFile, errorCodes, selectedOrder):
        for strategy in self.Strategies:
            strategy.PrintHeader(f'Source Display for {sourceFile}')
            strategy.HandleErrorCode(errorCodes, selectedOrder, strategy.ConvertData)    

