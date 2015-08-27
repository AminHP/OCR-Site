#! /usr/bin/python

from ann_trainer import ANN_Trainer

ann = ANN_Trainer()
ann.init([25, 30, 20, 3])

inputSamples   = []
inputSamples.append([0, 	0, 	1, 	0, 	0, 
		     0, 	0.5, 	0, 	0.5, 	0, 
		     0, 	1, 	0, 	1, 	0, 
		     0, 	1, 	1, 	1, 	0, 
		     1, 	0, 	0, 	0, 	1])

inputSamples.append([1, 	1, 	1, 	1, 	0, 
		     1, 	0, 	0, 	0, 	1, 
		     1, 	1, 	1, 	1, 	0, 
		     1, 	0, 	0, 	0, 	1, 
		     1, 	1, 	1, 	1, 	0])

inputSamples.append([1, 	1, 	1, 	1, 	1, 
		     1, 	0, 	0, 	0, 	0, 
		     1, 	0, 	0, 	0, 	0, 
		     1, 	0, 	0, 	0, 	0, 
		     1, 	1, 	1, 	1, 	1])

inputSamples.append([81.13636363636364, 42.5, 81.13636363636364, 42.5, 51.0, 52.15909090909091, 0.0, 54.09090909090909, 13.522727272727273, 17.0, 46.36363636363637, 0.0, 50.22727272727273, 46.36363636363637, 17.0, 48.29545454545455, 0.0, 50.22727272727273, 48.29545454545455, 31.166666666666668, 41.396103896103895, 44.70779220779221, 66.23376623376623, 62.922077922077925, 61.92857142857143])

desiredOutputs = []
desiredOutputs.append([1, 0, 0])
desiredOutputs.append([0, 1, 0])
desiredOutputs.append([0, 0, 1])
desiredOutputs.append([0, 1, 0])


ann.addData(inputSamples, desiredOutputs)

ann.train()
