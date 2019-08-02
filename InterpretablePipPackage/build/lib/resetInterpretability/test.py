from model.Model import Model
from model.SLIM.SLIMCode import SLIM
from model.baseline.DecisionTree import DecisionTree
from model.CORELS.CORELS import CORELS
from model.BOA.BOA import BayesianOrOf
import numpy as np 
import pandas as pd
import sys
import random
import subprocess
import os

if __name__ == '__main__' and len(sys.argv) > 1:
	slim, corels, bayesian, Decisiontree = False, False, False, False
	dataset = sys.argv[1]
	
	if len(sys.argv) > 2:
		if 'SLIM' in sys.argv:
			slim = True
		if 'CORELS' in sys.argv:
			corels = True
			lengthlist = 2
		if 'CORELS1' in sys.argv:
			corels = True
			lengthlist = 1
		if 'BayesianOrOf' in sys.argv:
			bayesian = True
		if 'DecisionTree' in sys.argv:
			Decisiontree = True
else:
	slim, corels, bayesian, Decisiontree = True, True, True, True
	dataset = 'bankruptcy'


RANDOMSEED = 0
random.seed(RANDOMSEED)

data = 'data/' + dataset + '_processed.csv'
my_data = np.genfromtxt(data, delimiter = ",", dtype = str)
X,Y = my_data[1:,1:].astype(float), my_data[1:,0].astype(float)
xlabels = my_data[0,1:]
ylabel = [my_data[0,0]]
train_ind = list(set(random.sample(range(len(X)), int (.8 * len(X)), )))

if 'bin' in sys.argv:
	for i in range(X.shape[1]):
		if len(set(X[: , i])) > 10:
			std = np.std(X[: , i])
			mean = np.mean(X[: , i])
			for j,entry in enumerate(X[: , i]):
				X[j,i] = round((entry - mean)/std) + 5


X_train = X[train_ind,:]
Y_train = Y[train_ind]
test_ind = [i for i in range(len(X)) if i not in train_ind]
X_test = X[test_ind, :]
Y_test = Y[test_ind]



if Decisiontree:
	dt = DecisionTree()
	dt.fit(X_train)
	result = dt.predict(X_test)

if slim:
	sl = SLIM()
	sl.fit(X_train,Y_train, xlabels, ylabel, dataset = dataset)
	result = sl.predict(X_test)
	acc,conf = sl.findAccuracy(result, Y_test)
	print(sl.get_name() + " got an accuracy of: " + str(acc) +  'and a confusion of: ' + conf )
	subprocess.call('subl ' + os.getcwd() + '/logs/SLIM/SLIM' + dataset, shell = True)

if corels:
	cr = CORELS()
	model = cr.fit(X_train,Y_train,xlabels, ylabel,  dataset = dataset, ruleListLength = lengthlist )
	print(cr.get_name() + ' model is: ' + str(model))
	o = cr.predict(X_test, xlabels)
	acc,conf = cr.findAccuracy(o, Y_test)
	print(cr.get_name() + " got an accuracy of: " + str(acc) + 'and a confusion of: ' + conf)
	subprocess.call('subl ' + os.getcwd() + '/logs/CORELS/CORELS' + dataset, shell = True)

if bayesian:
	boa = BayesianOrOf()
	boa.fit(X_train,Y_train,xlabels,ylabel, dataset = dataset)
	result = boa.predict(X_test,xlabels)
	acc,conf = boa.findAccuracy(result, Y_test)
	print(boa.get_name() + " got an accuracy: " + str(acc) + 'and a confusion of: ' + conf)
	subprocess.call('subl ' + os.getcwd() + '/logs/BOA/BOA' + dataset, shell = True)



