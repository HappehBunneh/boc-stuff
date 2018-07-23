import yaml
import os

class Print():
    def __init__(self, data, dataVariables):
        self.data = data
        self.dataVariables = dataVariables

    def getTerminalSize(self):
        width = int(os.popen('stty size', 'r').read().split()[1])
        return width
    
    def getLongestLength(self):
        if type(self.data) == dict:
            length = 0
            for i in self.data.keys():
                if len(i) > length:
                    length = len(i)
            for i in self.data.keys():
                if len(self.data[i]) > length:
                    length = len(self.data[i])
        elif type(self.data) == list:
            length = 0
            for i in self.data:
                if len(i) > length:
                    length = len(i)
        elif type(self.data) == str:
            length = len(self.data)
        return length

    def _print(self):
        self.width = self.getTerminalSize()
        self.lenData = self.getLongestLength()
        self.lenTab = len('\t'.expandtabs())
        self.lenStep = self.getLongestLength()*2+1+3*self.lenTab
        self.fit = self.width//self.lenStep
        self.text = ''
        b = 1
        for i in self.dataVariables:
            c = i
            d = self.data[i]
            while len(c) < self.lenData:
               c += ' '
            while len(d) < self.lenData:
               d += ' '
            if b > self.fit:
                self.text += '\n' + c + ':\t' + d + '\t\t' 
                b = 1
            else:
                self.text += c + ':\t' + d + '\t\t'
            b += 1
        return self.text