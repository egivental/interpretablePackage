import pandas as pd 
import numpy as np 
import os
import subprocess



def boaDataMake(X, Y, xlabels, ylabel):
	wd = os.getcwd()
	if not os.path.isdir('temp'):
		os.mkdir('temp')
	os.chdir('temp')
	f = open('X.txt', 'w+')
	xdic = {}
	X = pd.DataFrame(X, columns = xlabels)
	for label in X:
		for cat in set(X[label]):
			key = label + '_' + str(cat)
			xdic[key] = []
			for i in X[label]:
				if i == cat:
					xdic[key].append(1)
				else:
					xdic[key].append(0)
	X = pd.DataFrame.from_dict(xdic)
	X.to_csv(f, sep = ' ', index=False)
	f.close()
	if Y is not None:
		f = open('Y.txt', 'w+')
		for i in Y:
			f.write('%d\n' % i)
		f.close()
		print('done making temp data files for BOA')
	os.chdir(wd)
	return X
	
