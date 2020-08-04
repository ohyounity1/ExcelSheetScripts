def ErrorListToCSVDisplay(csvFile, objects, headers, msgConverter=None):
    headerString = ''

    for i in range(0, len(headers)):
        headerString += f'{headers[i]}'
        if(i < len(headers) - 1):
            headerString += ','
    csvFile.write(f'\n{headerString}')

    rowString = ''
    for obj in objects:
        rowString = ''
        for i in range(0, len(headers)):
            propertyName = headers[i]
            propertyValue = getattr(obj,propertyName)
            if(msgConverter is not None):
            	propertyValue = msgConverter(propertyName, propertyValue)
            rowString += propertyValue
            if(i < len(headers) - 1):
                rowString += ','
        csvFile.write(f'\n{rowString}')
