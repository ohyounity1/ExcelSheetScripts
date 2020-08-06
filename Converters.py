from lib.Constants import Constants

class ApplicationOutputConverters:
    
    def OutputReportTableDisplayMsg(name, data):
        if(name == Constants.ErrorDisplayMsgProperty):        
            displayMsg = ''
            if(len(data) > Constants.MaxValues.DisplayStringForTable):
                displayMsg = '{}...'.format(data[0:Constants.MaxValues.DisplayStringForTable])
            elif(len(data) > 0):
                displayMsg = data
            return displayMsg
        elif(name == Constants.ErrorDisplaysMsgProperty or name == Constants.ErrorIdProperty):
            return str(data)
        elif(name == Constants.ErrorTypeProperty):
            return str(data)
        return data
    
    def DataSourceCSVConversion(name, data):
        if(name == 'ErrorDisplayMsg'):
            if(len(data) > 0):
                data = data.replace('"', '""')
                return f'"{data}"'
            return data
        elif(name == Constants.ErrorTypeProperty):
            return str(data)
        else:
            rowString = f'{data}'
        return rowString
    