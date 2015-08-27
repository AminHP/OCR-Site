#! /usr/bin/python

from math import exp

class Neuron:
	def __init__(self):
		self.weights = []
		self.output  = 0.0
		self.errorGradient = 0.0

	def init(self, weightNum):
		import random
		self.weights = [random.uniform(-2.4, +2.4) for i in range(weightNum)]

	def activate(self, inputs):
		if len(inputs) != len(self.weights) - 1:
			print "Length of inputs and weights does not match!"

		output = 0.0
		for i in range(len(inputs)):
			output += inputs[i] * self.weights[i]
		output += self.weights[-1]

		if output < -200.0:
			output = -200.0

		output = 1.0 / (1.0 + exp((-output) * 0.667))
		#output = 2.0 / (1.0 + exp(-2.0 * output)) - 1.0;

		self.output = output

	def updateErrorGradient(self, error):
		self.errorGradient = error * self.output * (1.0 - self.output)

	def updateWeights(self, inputs, learningRate):
		for i in range(len(inputs)):
			self.weights[i] += learningRate * inputs[i] * self.errorGradient

	def __str__(self):
		result = ""

		for i in range(len(self.weights)):
			result += 'weight[' + str(i) + '] = ' + str(self.weights[i]) + '\n'

		result += 'output = ' + str(self.output)

		return result



if __name__ == '__main__':
	n = Neuron()
	n.init(3)
	n.activate([1, 1, 1])
	print n
