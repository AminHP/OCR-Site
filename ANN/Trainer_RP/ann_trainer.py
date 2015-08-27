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
		self.sum_errors_last = [1000, 1000]

		self.inputSamples   += inputSamples
		self.desiredOutputs += desiredOutputs

	def saveData(self, se, episode):
		data = [se, episode]

		if not models.Ann_trainer_rp_data.objects.filter(userid=self.userid):
			models.Ann_trainer_rp_data.objects.create(userid=self.userid, data=str(data))
		else:
			models.Ann_trainer_rp_data.objects.filter(userid=self.userid).update(data=str(data))

		del data

	def loadData(self):
		return 0

		if not models.Ann_trainer_rp_data.objects.filter(userid=self.userid):
			return 0

		data = eval(models.Ann_trainer_rp_data.objects.get(userid=self.userid).data)

		#del self.sum_errors_last
		#self.sum_errors_last = data[0]
		res = data[1]

		del data
		return res

	def train(self, max_error):
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

				self.ann.updateWeights_slope()

			#print sum_errors[0]
			if not episode % 10:
				if sum_errors[0] < self.sum_errors_last[0]:
					self.ann.saveData()
					#print "net data saved to file ..."
					self.saveData(sum_errors, episode)
					#print "trainer data saved to file ..."

					self.sum_errors_last[0] = sum_errors[0]
					self.sum_errors_last[1] = sum_errors[1]

				#print sum_errors
				#print "episode =", episode
				#print "---------------------------"

				if sum_errors[0] < max_error:
					break

			self.ann.updateWeights()

			del sum_errors
			episode += 1

