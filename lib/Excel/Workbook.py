import xlrd

class Workbook:
    def __init__ (self, fileName):
        self.wb = xlrd.open_workbook(fileName)
        