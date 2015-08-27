#! /usr/bin/python

from hidden_layer import HiddenLayer

class OutputLayer(HiddenLayer):
	pass


if __name__ == '__main__':
	o = OutputLayer()
	o.init(2, 3)
	o.activate([1, 1])
	print o
