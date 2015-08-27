#! /usr/bin/python

class InputLayer:
	def __init__(self):
		self.data = []

	def init(self, data):
		self.data = data

	def __str__(self):
		result = ""
		result += "data = " + str(self.data)
		return result


if __name__ == '__main__':
	l = InputLayer()
	l.init([1, 1, 1])
	print l
