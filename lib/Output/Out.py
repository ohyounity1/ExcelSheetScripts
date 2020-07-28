VerbosityNone = 0
VerbosityLow = 1
VerbosityMedium = 2
VerbosityHigh = 3

class Out:
    def __init__(self):
        self.Verbosity = VerbosityNone
    def Verbose(self, level, output):
        if(self.Verbosity >= level):
            print(output)
    def Error(self, output):
        print(output)
        exit()
    