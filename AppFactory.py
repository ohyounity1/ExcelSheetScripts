from pathlib import Path

from lib.DataSource import DataSources

from lib.Output import Out
from lib.Output import TableDisplay
from lib.Output import CsvDisplay

from lib.Utility import Debug

import Converters

class ReportAndExportAppBehavior:
	def __call__(self, sourceCenters, arguments):
		pass
	def __SourceStrategies__(self, sourceCenter, sourceStrategies):
		pass
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_value, exc_Trace):
		pass

class StandardReportAppBehavior(ReportAndExportAppBehavior):
	@Debug.DebugClassMethod
	def __SourceStrategies__(self, sourceCenter, sourceStrategies):
		sourceStrategies.append(DataSources.SourceStrategy(PrintHeader=Out.RegularPrint, 
			HandleErrorCode=TableDisplay.ErrorListToTableDisplay,
			ConvertData=Converters.ApplicationOutputConverters.OutputReportTableDisplayMsg))

class StandardExportAppBehavior(ReportAndExportAppBehavior):
	@Debug.DebugClassMethod
	def __SourceStrategies__(self, sourceCenter, sourceStrategies):
		exportFileName = f'{Path(sourceCenter.SourceName).stem}_Export.csv'
		self.ExportFile = open(exportFileName, 'w')
		sourceStrategies.append(DataSources.SourceStrategy(PrintHeader=self.ExportFile.write, 
			HandleErrorCode=lambda errors, selections, converter: CsvDisplay.ErrorListToCSVDisplay(self.ExportFile, errors, selections, converter),
			ConvertData=Converters.ApplicationOutputConverters.DataSourceCSVConversion))
	@Debug.DebugClassMethod
	def __exit__(self, exc_type, exc_value, exc_Trace):
		self.ExportFile.close()				

class ReportAndExportAppBehaviorDecorator(ReportAndExportAppBehavior):
	def __init__(self, reportBehavior: StandardReportAppBehavior, exportBehavior: StandardExportAppBehavior):
		self.ReportBehavior = reportBehavior
		self.ExportBehavior = exportBehavior
	@Debug.DebugClassMethod
	def __SourceStrategies__(self, sourceCenter, sourceStrategies):
		self.ReportBehavior.__SourceStrategies__(self.ReportBehavior, sourceCenter, sourceStrategies)
		self.ExportBehavior.__SourceStrategies__(self.ExportBehavior, sourceCenter, sourceStrategies)
	@Debug.DebugClassMethod
	def __exit__(self, exc_type, exc_value, exc_Trace):
		self.ExportBehavior.__exit__(self.ExportBehavior, exc_type, exc_value, exc_Trace)

class StandardReportAndExportAppBehavior(ReportAndExportAppBehaviorDecorator):
	def __call__(self, sourceCenters, arguments):
		for sourceCenter in sourceCenters:
			with self as disposable:
				sourceStrategies = list()
				disposable.__SourceStrategies__(sourceCenter, sourceStrategies)
				strategies = DataSources.SourceStrategyComposite(sourceStrategies)
				strategies(sourceCenter.SourceName, sourceCenter.SourceResults, arguments)

class AppBehaviors:
	def __init__(self, reportAndExportBehavior):
		self.ReportAndExportBehavior = reportAndExportBehavior

def AppFactory(arguments) -> AppBehaviors:
	reportAndExportBehavior = ReportAndExportAppBehavior()
	if(len(arguments.DiffActions) == 0 and len(arguments.ValidateActions) == 0 and len(arguments.JoinActions) == 0):
		reportAndExportBehavior = StandardReportAndExportAppBehavior(StandardReportAppBehavior, StandardExportAppBehavior)

	return AppBehaviors(reportAndExportBehavior)
