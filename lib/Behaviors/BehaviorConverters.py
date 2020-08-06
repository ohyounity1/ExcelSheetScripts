from ..Constants import Constants

class StandardBehaviorConverters:

    def ConvertErrorTypeDiffDisplayMsg(name, data):
        if(name == 'FirstValue' or name == 'SecondValue'):
            return str(data)
        return data
    
    def TableModuleValidationDataConverter(name, data):
        if(name == 'SuggestedModules'):
            return ','.join(data)
        return data
    
    def CsvModuleValidationDataConverter(name, data):
        if(name == 'SuggestedModules'):
            return f'"{StandardBehaviorConverters.TableModuleValidationDataConverter(name, data)}"'
        return data
    
    
    def TableModuleHasMsgValidationDataConverter(name, data):
        if(name == 'Message'):        
            displayMsg = data
            if(len(data) > Constants.MaxValues.DisplayStringForTable):
                displayMsg = '{}...'.format(data[0:Constants.MaxValues.DisplayStringForTable])
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