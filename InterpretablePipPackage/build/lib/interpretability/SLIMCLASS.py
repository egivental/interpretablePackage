import pandas as pd
import numpy as np
from .model.SLIM.train import main
import os
import datetime

class SLIM():
    def __init__(self, time_limit = 300, dataset = None, logging = True, verbose = False, epsilon = .001, logs = None, C0 = .001, bound = 5):
        self.name = "Rudin-SLIM"
        cwd = os.getcwd()
        if dataset == None: #if no dataset name, set to current time, otherwise keep
            self.dataset = str(datetime.datetime.now())
        else:
            self.dataset = dataset
        

        if logging:  #if logging save and makethe logs folder
            # If a logs was specified, make sure directory exists
            if logs != None:      
                if not os.path.isdir(cwd + logs):
                    print("The folder for logs does not exist. Now exiting")
                    exit(0)
                self.logs = cwd + logs
            #if it was not specified, make a folder called SLIMLogs
            else:
                if not os.path.isdir("SLIMLogs"):
                    os.mkdir("SLIMLogs")
                self.logs = "SLIMLogs"
            self.logFile = self.logs + self.dataset
        
        self.logging = logging
        self.verbose = False
        self.C0 = C0
        self.bound = bound
        self.epsilon = epsilon
        self.time_limit = time_limit


    def fit(self, X, Y, xlabels, ylabel, binning = False):
        if type(ylabel) == str:
            ylabel = [ylabel]
        def binner():    
            mean_std_dic = {}
            actually_binned = False
            for i in range(X.shape[1]):
                if len(set(X[: , i])) > 10:
                    actually_binned = True
                    std = np.std(X[: , i])
                    mean = np.mean(X[: , i])
                    mean_std_dic[xlabels[i]] = (mean, std)
                    for j,entry in enumerate(X[: , i]):
                        X[j,i] = round((entry - mean)/std) + 10
                else:
                    mean_std_dic[xlabels[i]] = (None, None)
            if actually_binned:
                return mean_std_dic
            else: 
                return {}

        mean_std_dic = {}
        if (bin):
            mean_std_dic = binner()
        Y = Y.reshape(Y.size,1)
        labels = np.concatenate([ylabel, xlabels])
        labels = labels.reshape(1, labels.shape[0])
        data = np.concatenate([Y,X], axis = 1).astype(int)
        

        ## CALL SLIM CODE
        self.stringModel, self.model = main(np.concatenate([labels, data], axis = 0), self.time_limit, self.bound, self.C0, self.epsilon)
        
        wd = os.getcwd()
        if self.logging:
            os.chdir(self.logs)  #change directory to Logging Directory
            f = open(self.logFile, 'w+')  #open the file
            f.write('Data Set Predicting: ' + ylabel[0] + '\nUsing Features:\n')  #write in the prediction and the features used
            if mean_std_dic:
                for i,key in enumerate(mean_std_dic):
                    if key != None:
                        f.write('\t'+ key + ': ' + str(set(X[:,i])) + ("0 corresponds to " + str(mean_std_dic[key][0]) + "Each shift is a standard deviation of: " + str(mean_std_dic[key][1])) + "\n")
                    else:
                        f.write('\t'+ key + ': ' + str(set(X[:,i])) + '\n') 
            else:
                for i,feature in enumerate(xlabels):
                    f.write('\t'+ feature + ': ' + str(set(X[:,i])) + '\n')
            f.write('\nmodel:\n' + self.stringModel + '\n\n') #write out the model
            f.write('Training Accuracy: ' + str(self.findAccuracy(self.predict(X), Y, log = False)) + '\n\n')  #State the training accuracy
            f.close()
            os.chdir(wd) #restore working directory
        return self.stringModel


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
