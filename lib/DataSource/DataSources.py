from collections import namedtuple

from ..Constants import Constants
from ..ErrorHandling import BadFileNameException
from ..ErrorCodes import ErrorCode
from ..Output import Out

def RetrieveAllResults(retriever):
    def __INTERNAL__(filePath):

        Out.VerbosePrint(Out.Verbosity.LOW, 'Source File Name: {0}'.format(filePath))
        errorCodes = retriever(filePath)

        if(errorCodes is None or len(errorCodes) == 0):
            Out.ErrorPrint('There were no error codes found in {}!'.format(filePath))

        return errorCodes
    return __INTERNAL__

def RetrieveErrorCodes(conversion):
    def __INTERNAL__(filePath):
        allErrorCodes = []

        if(filePath is not None):
            Out.VerbosePrint(Out.Verbosity.LOW, 'Reading in error codes from file of type {}'.format(filePath))
            conversion(filePath, allErrorCodes)
            Out.VerbosePrint(Out.Verbosity.LOW, 'Read in {} error codes from source {}'.format(len(allErrorCodes), filePath))
            return allErrorCodes
    
        raise BadFileNameException.BadFileNameException(extension)
    return __INTERNAL__


SourceCenter = namedtuple('SouceCenter', ['SourceName', 'SourceResults'])
SourceStrategy = namedtuple('SourceStrategy', ['PrintHeader', 'HandleErrorCode', 'ConvertData'])



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

