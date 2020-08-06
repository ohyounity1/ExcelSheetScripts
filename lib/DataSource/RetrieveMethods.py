from ..Output import Out
from ..ErrorHandling import BadFileNameException

def RetrieveAllResults(retriever):
    def __INTERNAL__(filePath):

        Out.VerbosePrint(Out.Verbosity.LOW, 'Source File Name: {0}'.format(filePath))
        errorCodes = retriever(filePath)

        if(errorCodes is None or len(errorCodes) == 0):
            Out.ErrorPrint('There were no error codes found in {}!'.format(filePath))

        filteredList = []

        for ec in errorCodes:
            if(ec not in filteredList):
                filteredList.append(ec)
            else:
                Out.VerbosePrint(Out.Verbosity.LOW, f'Filtering out error code {ec} since it appears to be repeating!')

        Out.VerbosePrint(Out.Verbosity.LOW, 'Read in {} error codes from source {} after filtering'.format(len(filteredList), filePath))
        return filteredList
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