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
        self.lenStep = self.getLongestLength()*2+9+16
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
            if b > 3:
                self.text += '\n' + c + ':\t' + d + '\t\t' 
                b = 1
            else:
                self.text += c + ':\t' + d + '\t\t'
            b += 1
        return self.text
        
            


'''
def getTerminalSize():
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns

def getLongestLength(thing):
    if type(thing) ==  dict:
        a = thing.keys()
        length = getLongestLength(a)
        for i in a:
            if len(thing[i]) > length:
                length = len(thing[i])
        return length

    if type(thing) == list:
        length = 0
        for i in thing:
            if len(i) > length:
                length = len(i)
        return length

    if type(thing) == str:
        return len(thing)

with open('config.yaml', 'r') as file:
    config = yaml.load(file)
    dataVariables = config['dataVariables']

with open('buffer.txt', 'r') as buffer:
    try:
        data = eval(buffer.read())
    except (Exception, EOFError, IOError, SyntaxError):
        data = buffer.read()
    
dataVariables = [i for i in dataVariables if 'IGNORE' not in i]

height, width = getTerminalSize()
width = int(width)
a = ''
lenOfWord = getLongestLength(data)
lenOfBit = getLongestLength(data)*2+9+16
fit = width//lenOfBit
b = 1
for i in dataVariables:
    c = i
    d = data[i]
    while len(c) < lenOfWord:
        c += ' '
    while len(d) < lenOfWord:
        d += ' '
    if b > 3:
        a += '\n' + c + ':\t' + d + '\t\t' 
        b = 1
    else:
        a += c + ':\t' + d + '\t\t'
    b += 1
print a
for i in dataVariables:
    if len(a + i + ':\t' + data[i] + '\t\t') % width < width:
        a += i + ':\t' + data[i] + '\t\t'
    else:
        a += '\n' + i + ':\t' + data[i] + '\t\t'
print a
'''