#! /usr/bin/python

from ann import ANN

import polls.models as models


class ANN_Trainer:
	def __init__(self, userid):
		self.userid = userid

		self.inputSamples = []
		self.desiredOutputs = []

		for s in models.Ann_samples.objects.filter(userid=userid):
			self.inputSamples.append(eval(s.input))
			self.desiredOutputs.append(eval(s.output))

		self.learningRate = 0.1

		self.init()

	def __del__(self):
		del self.inputSamples
		del self.desiredOutputs

	def init(self):
		self.ann = ANN(self.userid)
		if self.ann.loadData():
			return

		self.ann.init([25, 30, 20, 26])


	def addData(self, inputSamples, desiredOutputs):
		self.sum_errors_prev = [1000, 1000]
		self.sum_errors_last = [1000, 1000]

		self.inputSamples += inputSamples
		self.desiredOutputs += desiredOutputs

	def updateLearningRate(self, sum_errors, sum_errors_prev):
		err = sum_errors[0]
		err_prev = sum_errors_prev[0]

		if err_prev == 0.0:
			return

		if err / err_prev > 1.04:
			self.learningRate *= 0.7
		if err < err_prev:
			self.learningRate *= 1.05

		if self.learningRate > 3.0:
			self.learningRate = 0.1

	def saveData(self, se, episode):
		data = [se, self.sum_errors_last, self.learningRate, episode]

		if not models.Ann_trainer_data.objects.filter(userid=self.userid):
			models.Ann_trainer_data.objects.create(userid=self.userid, data=str(data))
		else:
			models.Ann_trainer_data.objects.filter(userid=self.userid).update(data=str(data))

		del data


	def loadData(self):
		if not models.Ann_trainer_data.objects.filter(userid=self.userid):
			return 0

		data = eval(models.Ann_trainer_data.objects.get(userid=self.userid).data)

		#del self.sum_errors_prev
		#del self.sum_errors_last
		#self.sum_errors_prev = data[0]
		#self.sum_errors_last = data[1]
		self.learningRate = data[2]
		res = data[3]

		del data
		return res

	def train(self, max_error):
		self.sum_errors_prev = [1000, 1000]
		self.sum_errors_last = [1000, 1000]

		episode = self.loadData()

		while True:
			sum_errors = [0, 0]

			for i in range(len(self.inputSamples)):
				self.ann.activate(self.inputSamples[i])

				err = self.ann.updateErrorGradients(self.desiredOutputs[i])
				sum_errors[0] += err[0]
				sum_errors[1] += err[1]
				del err

				if i < len(self.inputSamples) - 1:
					self.ann.updateWeights(self.learningRate)

			self.updateLearningRate(sum_errors, self.sum_errors_prev)

			if not episode % 10:
				if sum_errors[0] < self.sum_errors_last[0]:
					self.ann.saveData()
					#print "net data saved to file ..."
					self.saveData(sum_errors, episode)
					#print "trainer data saved to file ..."

					self.sum_errors_last[0] = sum_errors[0]
					self.sum_errors_last[1] = sum_errors[1]

				# print sum_errors, self.learningRate
				#print "episode =", episode
				#print "---------------------------"

				#if sum_errors[0] < 1.5:
				if sum_errors[0] < max_error:
					break

			self.ann.updateWeights(self.learningRate)

			del self.sum_errors_prev
			self.sum_errors_prev = sum_errors
			episode += 1

