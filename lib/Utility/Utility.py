from ..Constants import Constants

def IntrospectErrorCodes(errorCodes):
    selectionOfItems = [x for x in dir(errorCodes[0]) if (x.startswith(Constants.PrivatePropertySuffix) == False) if (x.endswith(Constants.PrivatePropertySuffix) == False)]
    return selectionOfItems
    
def TranslateExcelString(excelString):
    return excelString.translate(str.maketrans('', '', ' \t\n\r'))
    