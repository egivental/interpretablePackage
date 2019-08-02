import os
import subprocess
import sys
import numpy as np
import pandas as pd
import string
from .dataMaker import CorelsDataMake
import copy


#This method accepts a string which contains a definition of a dictionary 
#it returns a dictionary, which contains certain inputs that correspond to an output
#Ex: {X1:4,X2:3,Y:1} it is called by the fit in CORELS 
#input: a string which contains a dictionary with {XXX,YYY}
def findDictionaries(line):  
    if 'if' in line:  #if not the last line of the rule list
        then = line.split('then')  #split between the rules and the outcome
        line = then[0]
        then = eval(then[1])
        i = 0
        while(line[i] != '(' ):  #ignore the text before the dictionary definition
            i +=1
        i+=1
        if line[i] == '{':
            i+=1
            dict = '{'
            while(line[i] != '}'):  #until we finish finding all the rules, parse the text
                dict += line[i]
                i+=1
            dict += '}'  #close the dictionary
        elif line[i] == '0':
            dict = '{0:0}'
        elif line[i] == '1':
            dict = '{1:1}'
        dict = eval(dict)  #create the dictionary
        dict.update(then)  #add in the outcome to the dictionary
    else:  #if there were no rule; this was the else statement
        dict = ''  
        i = 0
        while dict != '{':  #get to the dictionary
            dict = line[i]
            i += 1
        while '}' not in dict:  #finish the dictionary
            dict += line[i]
            i+=1
        dict = eval(dict)  #create the dictionary
    return dict


class CORELS():
    def __init__(self):
        self.model = 'not run'
        self.output = ''
        self.name = "<Rudin-CORELS>"

        cwd = os.getcwd()
        if not os.path.isdir('temp'):
            os.mkdir('temp')
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        os.chdir(cwd + '/logs/')
        if not os.path.isdir('CORELS'):
            os.mkdir('CORELS')
        os.chdir(cwd)
        self.logs = os.getcwd() + '/logs/CORELS/'



    ###fit accepts an X matrix, a Y matrix both must have equal length, 
    ###optionally it accepts xlabels, and ylabels, a maximum length of each rule list (max 2)
    ###and a log file path 
    ### Inputs: X (2D matrix),Y (Vector) OPTIONAL INPUTS: xlabels (list), ylabel(list), ruleListLength (1 or 2), logfile (str)
    def fit(self, X, Y, xlabels = 'not_defined', ylabel = ['Y'], ruleListLength = 2, dataset = None): 
        
        ### fixing data for parsing ###
        self.lengthList = ruleListLength
        if type(ylabel) is str:
            ylabel = [ylabel]
        Xstr,Ystr = X.astype(str) , Y.astype(str)  #we convert the data to strings for easier getting rid of spaces
        if type(xlabels) is str:  #in case the labels were not defined
            xlabels = list(range(Xstr.shape[1]))  
        else:
            for i in range(len(xlabels)):  #we get rid of spaces
                xlabels[i] = str(xlabels[i]).replace(' ', '_')  # we set them to the numbers from 0 to num_features
        ylabel[0] = str(ylabel[0]).replace(' ', '_') #get rid of spaces in ylabels

        ### making temp data files and log files ### 
        wd = os.getcwd()  #we get the currect wd to correctly move around for calls later
        dataPath = wd + '/temp/train'  #we set the datapath for temp txt file 
        if dataset == None:
            self.logFile = 'CORELSpredicting' + ylabel[0] #we set the datapath for the logfile
        else:
            self.logFile = 'CORELS' + dataset 
        CorelsDataMake(Xstr, Ystr, xlabels, ylabel, ruleListLength) #Call this function to make txt files that 
        print("done making CORELS data file")
        #have one hot encoded data
        f = open(wd + '/temp/templog.txt', 'w+')

        ### calling subprocesses to call CORELS src code ###
        os.chdir(wd + "/model/CORELS/corels_master/src/")  #change directory to src directory
        new_call = './corels -r 0.0005 -c 2 -p 1 -L ' + dataPath + '.out ' +  dataPath + '.label ' 
        subprocess.call('make', shell = True, stdout = f)  #use their make from their makefile
        subprocess.call(new_call, shell = True, stdout = f) #call their method, writing to logfile
        f.close() #close the file so that now we can read from it 
        os.chdir(wd)
        ### parsing the results from the logfile ### 
        f = open(wd +  '/temp/templog.txt', 'r') #open the file for reading
        line = f.readline()  #read lines until we find the optimal rule list line
        while(line!= 'OPTIMAL RULE LIST\n'):  
            line = f.readline()
        line = ''
        newLine = 'if'      
        while 'if' in newLine:  #until we get to the end of the non else statements
            newLine = f.readline()
            line += newLine

        rules = line.split('\n')  #make an array of with all the rules
        ruleList = [] # initialize final output, list of dictionaries
        for rule in rules: #for each string in rules
            if rule != '\n' and rule != '': 
                ruleList.append(findDictionaries(rule))     #find the dictionary in the string

        ### printing and saving the results in log file and restoring working directory ###
        self.model = ruleList  #save the rules and the feature that is being classified
        self.output = ylabel[0].replace('\"', '')
        self.xlabels = xlabels

        f.close()  #close file
        subprocess.call('rm -R temp', shell = True)

        self.logs = wd + '/logs/CORELS/'
        os.chdir(self.logs)  #change directory to Logging Directory
        f = open(self.logFile, 'w+')  #open the file
        f.write('Data Set Predicting: ' + ylabel[0] + '\nUsing Features:\n')  #write in the prediction and the features used
        for i,feature in enumerate(xlabels):
            f.write('\t'+ feature.strip('"') + ': ' +  str(set(X[:,i])) + '\n')  
        f.write('\nmodel:\n' + line + '\n\n') #write out the model
        f.write('Training Accuracy: ' + str(self.findAccuracy(self.predict(X, xlabels), Y, log = False)) + '\n\n')  #State the training accuracy
        f.close()
        os.chdir(wd) #restore working directory
        wd = os.getcwd()
        #print(wd)
        return ruleList  #print out the rules

    #inputs: Accepts an X matrix, along with an optional set of x labels, which should be a matrix
    def predict(self, X, xlabels = ''):
        
        ### checking xlabels ###
        assert(self.model != 'not run'), 'the model has not yet been run. run CORELS.fit()'
        if type(xlabels) is string:  #in case labels not given
            xlabels = range(X.shape[1])  #the labels become numbers from 1-5
        #assert(set(xlabels) == set(xlabels)), 'the labels do not match or not given'
        
        ### reorienting data and turning into dictionary###
        X = pd.DataFrame(X, columns = xlabels)  
        X = X.transpose()
        X = X.to_dict()

        ### initializing and making an array of outcomes that will have the same length as X ###-
        outcomes = []  # empty array for outcomes
        for row in X.values(): #get the dictionary definition of each input
            extra = copy.deepcopy(self.model) #make a deepcopy of the model so that it can be changed
            for key in row:  
                row[key.replace('\"', '')] = row.pop(key)  #for each input remove spaces
            for dic in extra:    
                outcome = dic.pop(self.output) #pop the outcome if this given dictionary in the 
                #rule list turns out to be the right one
                if dic == {1:1}:
                    outcomes.append(outcome)
                    break;
                if dic == {0:0}:
                    outcomes.append(1-outcome)
                    break;
                if all(key in row and row[key] == dic[key] for key in dic):  #if the rule list dictionary is contained 
                #by the datapoint, we return the output of that rule list dictionary
                    outcomes.append(outcome)
                    break;
        return outcomes


    ### Tells you the accuracy of your algorithm by comparing predictions to actual outputs ###
    ### inputs: 2 numpy vectors of equal length ### 
    ### outputs: A floating point number representing the fraction that were correctly predicted
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
            f.write('Testing Accuracy: ' + str((acc,confusionString)))
            f.close()
            os.chdir(wd)
        return acc, confusionString

    ### returns the name of the algorithm ### 
    def get_name(self):
        return self.name



