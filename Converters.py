from lib.Constants import Constants

def ConvertErrorTypeDiffDisplayMsg(name, data):
    if(name == 'FirstValue' or name == 'SecondValue'):
        return str(data)
    return data

def ConvertTableDisplayMsg(name, data):
    if(name == Constants.ErrorDisplayMsgProperty):        
        displayMsg = ''
        if(len(data) > Constants.MaxDisplayStringForTable):
            displayMsg = '{}...'.format(data[0:Constants.MaxDisplayStringForTable])
        elif(len(data) > 0):
            displayMsg = data
        return displayMsg
    elif(name == Constants.ErrorDisplaysMsgProperty or name == Constants.ErrorIdProperty):
        return str(data)
    elif(name == Constants.ErrorTypeProperty):
        return str(data)
    return data

def ConvertCSVOutput(name, data):
    if(name == 'ErrorDisplayMsg'):
        data = data.replace('"', '""')
        rowString = f'"{data}"'
    else:
        rowString = f'{data}'
    return rowString

def TableModuleValidationDataConverter(name, data):
    if(name == 'SuggestedModules'):
        return ','.join(data)
    return data

def CsvModuleValidationDataConverter(name, data):
    if(name == 'SuggestedModules'):
        return f'"{TableModuleValidationDataConverter(name, data)}"'
    return data


def TableModuleHasMsgValidationDataConverter(name, data):
    if(name == 'Message'):        
        displayMsg = data
        if(len(data) > Constants.MaxDisplayStringForTable):
            displayMsg = '{}...'.format(data[0:Constants.MaxDisplayStringForTable])
        return displayMsg
    if(name == 'HasMsgValue' or name == 'SuggestedValue'):
        return str(data)
    return data

def CsvModuleHasMsgValidationDataConverter(name, data):
    if(name == 'Message'):        
        data = data.replace('"', '""')
        return f'"{data}"'
    if(name == 'HasMsgValue' or name == 'SuggestedValue'):
        return str(data)
    return data
