from ..Output import Out
from ..ErrorHandling import BadFileNameException

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