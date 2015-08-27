#! /usr/bin/python

from ann_trainer import ANN_Trainer

ann = ANN_Trainer()
ann.init([25, 50, 50, 25])

inputSamples   = [[(float(j) / 100.0) for i in range(25)] for j in range (100)]
desiredOutputs = [[(float(j) / 100.0) for i in range(25)] for j in range (100)]
ann.addData(inputSamples, desiredOutputs)

ann.train()
