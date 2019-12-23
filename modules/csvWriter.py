import os
import sys

class csvWriter():
    def __init__(self, fileName):
        self.file = fileName
        os.environ["FILENAME"] = fileName

    def writeToFile(self, dataToWrite):
        with open(fileName, "a") as f:
            f.write(dataToWrite)
        return True
