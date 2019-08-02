import pandas as pd 
import numpy as np

###Creates 2 one hot encoded temporary data files that are required for CORELS to run
###inputs: X, Y, xlabels, ylabel, and ruleLength (either 1 or 2)
def CorelsDataMake(X, Y, xlabels, ylabel, ruleLength = 2):
	### processing inputs and creating temp file ### 
	for i,j in enumerate(xlabels):
		xlabels[i] = '"' + j.strip('"').strip("'") + '"'
	ylabel[0] = '"' + ylabel[0].strip('"').strip("'") + '"'
	X = pd.DataFrame(X, columns = xlabels, dtype = str)	
	Y = pd.DataFrame(Y, columns = ylabel, dtype = str)
	f = open('temp/train.label', "w+")
	
	### creating label file ###
	text = ''
	datapoints = Y.shape[0]  #num datapoints stored
	for column in Y:  #there should only be one
		categories = set(Y[column])  #should be 1/0
		assert(len(categories) == 2), 'should have 2 potential classifications'
		for i in categories:  #for each category within the feature
			text += '{%s:%s}' % (column.replace(" ", "_"), str(i).replace(' ', '_')) #remove spaces
			for j in Y[column]:  #for each datapoint in the column
				if j == i:  #this one hot encodes 
					text+= ' 1'
				else: 
					text += ' 0'
			text+= '\n'
	f.write(text)
	f.close()


	### creating input file ### 
	f = open('temp/train.out', 'w+')
	for column in X: #for each feature
		column = str(column)  #turn it into string for string 
		text = ''
		categories = set(X[column])  #find the categories in that column
		#print(X[column])
		#if len(categories) > 5:
			##a, b = np.histogram(X[column].astype(float), 'auto')
			#X[column] = pd.cut(X[column], b)
			#categories = set(X[column])
		for i in categories:  #this one hot encodes the data
			text += '{%s:%s}' % (column.replace(" ", "_"), str(i).replace(' ', '_'))
			for j in X[column]:
				if j == i:
					text+= ' 1'
				else: 
					text += ' 0'
			text+= '\n'
		f.write(text)
	if ruleLength == 1:  ### IF RULELENGTH == 1, we stop
		f.close()
		return 1

	### if the rulelength is 2, we do one hot encoding for every pair of categories in different features ###
	for i in range(len(xlabels)):
		ith = xlabels[i]
		for j in range(i+1, len(xlabels)):
			jth = xlabels[j]
			for cat in set(X[ith]):
				for cat2 in set (X[jth]):
					text = '{%s:%s,%s:%s}' % (ith.replace(" ", "_"), str(cat).replace(' ', '_'), jth.replace(' ', '_'), str(cat2).replace(' ', '_'))
					for k in range(datapoints):
						if X[ith][k] == cat and X[jth][k] == cat2:
							text += ' 1'
						else:
							text += ' 0'
					text+= '\n'
				f.write(text)
	#if ruleLength == 2:  
	#	f.close()
	#	return 2


