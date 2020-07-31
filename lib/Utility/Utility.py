from ..Constants import Constants

def IntrospectObject(object, desiredOrder, filter=None):
    def __Inner__(filter, object):
        if(filter == None): 
            return true;
        return filter(object)
    finalSelection = []

    #for desired in desiredOrder:
    #	if(__Inner__(filter, desired)):
    #		for x in dir(object):
    #			if (x.startswith(Constants.PrivatePropertySuffix) == False) and (x.endswith(Constants.PrivatePropertySuffix) == False) and x == desired:
    #				finalSelection.append(desired)

    return [desired for desired in desiredOrder if __Inner__(filter, desired) 
        for x in dir(object) if (x.startswith(Constants.PrivatePropertySuffix) == False) if (x.endswith(Constants.PrivatePropertySuffix) == False) if x==desired]
    
def TranslateExcelString(excelString):
    return excelString.translate(str.maketrans('', '', ' \t\n\r'))
    