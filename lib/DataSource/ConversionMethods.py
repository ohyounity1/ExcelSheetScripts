from pathlib import Path

from . import ExcelConversion
from . import JsonConversion

from . import DataSources
__DataSources__ = {
    '.xls' : ExcelConversion.ExcelSheetErrorCodeListing,
    '.xlsx': ExcelConversion.ExcelSheetErrorCodeListing,
    '.json': JsonConversion.JsonFileErrorCodeListing
}

def DataSourceConversion(file):
	index = Path(file).suffix
	return __DataSources__[index](file)
