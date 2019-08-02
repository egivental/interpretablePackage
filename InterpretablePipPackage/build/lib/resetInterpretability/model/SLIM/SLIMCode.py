import pandas as pd
import numpy as np
from .train import main
import os

class SLIM():
    def __init__(self):
        self.name = "<Rudin-SLIM>"
        cwd = os.getcwd()
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        os.chdir(cwd + '/logs/')
        if not os.path.isdir('SLIM'):
            os.mkdir('SLIM')
        os.chdir(cwd)


    def fit(self, X, Y, xlabels, ylabel, dataset = None):
        Y = Y.reshape(Y.size,1)
        labels = np.concatenate([ylabel, xlabels])
        labels = labels.reshape(1, labels.shape[0])
        data = np.concatenate([Y,X], axis = 1).astype(int)
        self.stringModel, self.model = main(np.concatenate([labels, data], axis = 0))
        print(self.model)
        
        if dataset == None:
            self.logFile = 'SLIMpredicting' + ylabel[0] 
        else:
            self.logFile = 'SLIM' + dataset
        wd = os.getcwd()
        self.logs = wd + '/logs/SLIM/'
        os.chdir(self.logs)  #change directory to Logging Directory
        f = open(self.logFile, 'w+')  #open the file
        f.write('Data Set Predicting: ' + ylabel[0] + '\nUsing Features:\n')  #write in the prediction and the features used
        for i,feature in enumerate(xlabels):
            f.write('\t'+ feature + ': ' + str(set(X[:,i])) + '\n')  
        f.write('\nmodel:\n' + self.stringModel + '\n\n') #write out the model
        f.write('Training Accuracy: ' + str(self.findAccuracy(self.predict(X), Y, log = False)) + '\n\n')  #State the training accuracy
        f.close()
        os.chdir(wd) #restore working directory


    def predict(self, X):
        outcomes = np.ones(len(X))
        for x in range(len(X)):
            y = X[x].dot(self.model[1:]) + self.model[0]
            if (y >= 0):
                outcome = 1
            else:
                outcome = 0
            outcomes[x] = outcome
        return outcomes

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
            f = open(self.logFile, 'a')
            f.write('Testing Accuracy: ' + str((acc, confusionString))) 
            f.close()
            os.chdir(wd)
        return acc, confusionString

    def get_name(self):     
        return self.name
