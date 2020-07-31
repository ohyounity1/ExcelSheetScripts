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

def Tie(x, y): 
    _0 = (x,y)
    _1 = (y,x)
    def Untie():
        return (_0[0], _0[1])
    return (_0, _1, Untie)
    