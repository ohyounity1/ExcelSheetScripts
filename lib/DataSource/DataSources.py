from ..Constants import Constants
from ..ErrorHandling import BadFileNameException
from ..ErrorCodes import ErrorCode
from ..Output import Out

from . import ExcelConversion
from . import JsonConversion

__DataSources__ = {
    '.xls' : ExcelConversion.ExcelSheetErrorCodeListing,
    '.xlsx': ExcelConversion.ExcelSheetErrorCodeListing,
    '.json': JsonConversion.JsonFileErrorCodeListing
}

def RetrieveErrorCodes(filePath) -> [ErrorCode.ErrorCode]:
    from pathlib import Path

    extension = Path(filePath).suffix

    allErrorCodes = []

    source = __DataSources__.get(extension)

    if(source is not None):
        Out.VerbosePrint(Out.Verbosity.LOW, 'Reading in error codes from file of type {}'.format(extension))
        source(filePath, allErrorCodes)
        Out.VerbosePrint(Out.Verbosity.LOW, 'Read in {} error codes from source {}'.format(len(allErrorCodes), filePath))
        return allErrorCodes

    raise BadFileNameException.BadFileNameException(extension)