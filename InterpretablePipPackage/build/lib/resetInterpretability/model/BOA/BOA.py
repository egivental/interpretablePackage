import pandas as pd
import numpy as np
from .dataMaker import *
from pandas.io.parsers import read_csv
from .BOAmaster.BOAmodel import * 
from collections import defaultdict
import subprocess
import sys
import os



class BayesianOrOf():
    def __init__(self):
        self.name = "Bayesian or-of-and algorithm (BOA)"
        cwd = os.getcwd()
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        os.chdir(cwd + '/logs/')
        if not os.path.isdir('BOA'):
            os.mkdir('BOA')
        os.chdir(cwd)

    def fit(self, X, Y, xlabels = 'undef', ylabel = 'Y', dataset = None):

        if type(ylabel) is str:
            ylabel = [ylabel]

        for i,j in enumerate(xlabels):
            xlabels[i] = j.strip('"')
        ylabel = [ylabel[0].strip('"')]
        if type(xlabels) is str:
            xlabels = range(len(X))
        boaDataMake(X, Y, xlabels, ylabel)
        N = 2000      # number of rules to be used in SA_patternbased and also the output of generate_rules
        Niteration = 500  # number of iterations in each chain
        Nchain = 2         # number of chains in the simulated annealing search algorithm
        supp = 5           # 5% is a generally good number. The higher this supp, the 'larger' a pattern is
        maxlen = 3         # maxmum length of a pattern

        alpha_1 = 500
        beta_1 = 1
        alpha_2 = 500
        beta_2 = 1

        if dataset == None:
            dataset = 'predicting' + ylabel[0]
        self.logfile = 'BOA' + dataset

        df = read_csv('temp/X.txt', header = 0, sep = " ")
        Y = np.loadtxt(open('temp/Y.txt', 'rb'), delimiter = " ")
        lenY = len(Y)
        
        self.model = BOA(df,Y)
        self.model.generate_rules(supp,maxlen,N)
        self.model.set_parameters(alpha_1,beta_1,alpha_2,beta_2,None,None)
        self.rules = self.model.SA_patternbased(Niteration,Nchain,print_message=False)
        self.ylabel = ylabel[0]


        ### MAKE LOG ###
        cwd = os.getcwd()
        self.logs = cwd + '/logs/BOA/'
        os.chdir(self.logs)  #change directory to Logging Directory
        
        f = open(self.logfile, 'w+')  #open the file
        f.write('Data Set Predicting: ' + ylabel[0] + '\nUsing Features:\n')  #write in the prediction and the features used
        for i,feature in enumerate(xlabels):
            f.write('\t'+ feature + ': ' + str(set(X[:,i])) + '\n')  
        f.write('\nmodel: ' + str(self.rules) + '\n\n') #write out the model
        f.write('Training Accuracy: ' + str(self.findAccuracy(self.predict(X, xlabels), Y, log = False)) + '\n\n')  #State the training accuracy
        f.close()
        os.chdir(cwd)
        subprocess.call('rm -R temp', shell = True)
        return self.rules 

    def predict(self, X, xlabels):
        toRet = predict(self.rules, boaDataMake(X, None, xlabels, None))
        subprocess.call('rm -R temp', shell = True)
        return toRet
    
    def findAccuracy(self, predictions, Y, log = True):
        assert(len(predictions) == len(Y)), 'Y and predictions must have the same length'
        correct, truePos, trueNeg, falsePos, falseNeg  = 0,0,0,0,0
        for i in range(len(Y)):
            if predictions[i] == 1 and Y[i] == 1:
                truePos += 1
                correct += 1
            elif predictions[i] == 0 and Y[i] == 0:
                trueNeg += 1
                correct += 1
            elif predictions[i] == 1 and Y[i] == 0:
                falsePos += 1
            elif predictions[i] == 0 and Y[i] == 1:
                falseNeg += 1
        confusionString = 'TP: ' + str(truePos) + ' TN: ' + str(trueNeg) + ' FP: ' + str(falsePos) + ' FN: ' + str(falseNeg)
        acc = correct/len(Y)
        if log:
            wd = os.getcwd()
            os.chdir(self.logs)
            f = open(self.logfile, 'a')
            f.write('Testing Accuracy: ' + str((acc,confusionString)))
            f.close()
            os.chdir(wd)
        return acc, confusionString

    def get_name(self):
        return self.name
