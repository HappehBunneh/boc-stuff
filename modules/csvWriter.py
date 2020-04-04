#!/usr/bin/python3
import os
import sys

FILE_LOCATION = "/var/log/hymera/"

class csvWriter():
	def __init__(self, fileName):
		self.file = FILE_LOCATION + fileName
		os.environ["FILENAME"] = FILE_LOCATION + fileName
		with open(self.file, "w") as f:
			pass

	def writeToFile(self, dataToWrite):
		with open(self.file, "a") as f:
			f.write(dataToWrite+"\n")
		return True

if __name__ == "__main__":
	a = csvWriter("test.txt")
	a.writeToFile("a")
	a.writeToFile("b")
	a.writeToFile("c")