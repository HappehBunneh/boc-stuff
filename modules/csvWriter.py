#!/usr/bin/python3
import os
import sys

class csvWriter():
    def __init__(self, fileName):
        self.file = fileName
        os.environ["FILENAME"] = fileName

    def writeToFile(self, dataToWrite):
        with open(self.file, "a") as f:
            f.write(dataToWrite+"\n")
        return True

if __name__ == "__main__":
    a = csvWriter("test.txt")
    a.writeToFile("a")
    a.writeToFile("b")
    a.writeToFile("c")
