#! /usr/bin/python

from neuron import Neuron

class HiddenLayer:
	def __init__(self):
		self.neurons = []
		self.outputs = []

	def init(self, inputNum, neuronNum):
		self.neurons = [Neuron() for i in range(neuronNum)]
		self.outputs = [0 for i in range(neuronNum)]

		for n in self.neurons:
			n.init(inputNum)

	def activate(self, inputs):
		if len(inputs) != len(self.neurons[0].weights) - 1:
			print "Length of inputs and weights does not match!"

		for n in self.neurons:
			n.activate(inputs)

		for i in range(len(self.neurons)):
			self.outputs[i] = self.neurons[i].output

	def updateErrorGradients(self, nextLayer):
		for i in range(len(self.neurons)):
			error = 0.0

			for j in range(len(nextLayer.neurons)):
				error += nextLayer.neurons[j].weights[i] * nextLayer.neurons[j].errorGradient

			self.neurons[i].updateErrorGradient(error)

	def updateWeights_slope(self, inputs):
		for n in self.neurons:
			n.updateWeights_slope(inputs)

	def updateWeights(self):
		for n in self.neurons:
			n.updateWeights()

	def __str__(self):
		result = ""

		for i in range(len(self.neurons)):
			result += "--->neuron[" + str(i) + "]:\n" + str(self.neurons[i]) + '\n'
		result += "outputs = " + str(self.outputs) + '\n'

		return result



if __name__ == '__main__':
	h = HiddenLayer()
	h.init(2, 3)
	h.activate([1, 1])
	print h
