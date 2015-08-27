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

		self.weights_slope      = [0.0 for i in range(weightNum)]
		self.weights_slope_prev = [0.0 for i in range(weightNum)]

		self.deltha  = [0.1 for i in range(weightNum)]
		self.u_plus  = 1.2
		self.u_minus = 0.5


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

	def updateWeights_slope(self, inputs):
		for i in range(len(inputs)):
			self.weights_slope[i] += inputs[i] * self.errorGradient
		self.weights_slope[-1] += 1.0 * self.errorGradient

	def updateWeights(self):
		weights            = self.weights
		weights_slope      = self.weights_slope
		weights_slope_prev = self.weights_slope_prev
		deltha             = self.deltha

		for i in range(len(weights_slope)):
			if weights_slope[i] * weights_slope_prev[i] >= 0.0:
				deltha[i] *= self.u_plus

			else:
				deltha[i] *= self.u_minus
				weights_slope[i] = 0.0


			if deltha[i] > 50.0:
				deltha[i] = 50.0
			if deltha[i] < 0.000001:
				deltha[i] = 0.000001

			if weights_slope[i] < 0.0:
				weights[i] -= deltha[i]
			else:
				weights[i] += deltha[i]

			weights_slope_prev[i] = weights_slope[i]
			weights_slope[i] = 0.0

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
