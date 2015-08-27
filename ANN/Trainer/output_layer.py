#! /usr/bin/python

from hidden_layer import HiddenLayer

class OutputLayer(HiddenLayer):
	def updateErrorGradients(self, desiredOutput):
		sum_error = [0, 0]

		for i in range(len(self.outputs)):
			error = desiredOutput[i] - self.outputs[i]
			self.neurons[i].updateErrorGradient(error)

			sum_error[0] += abs(error)
			sum_error[1] += error ** 2.0

		return sum_error



if __name__ == '__main__':
	o = OutputLayer()
	o.init(2, 3)
	o.activate([1, 1])
	print o
