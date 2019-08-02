This is a library with 3 interepretable machine learning methods, wrapped with logging and side by side comparison. They can be used as normal scikit learn models, with fit, predict, and find_accuracy methods. Or, a script can be run on a data set, which will run all three and return logs and accuracies. 



Sample run:

from interpretability import SLIM
import numpy as np
import random

if __name__ == "__main__":
    datafilename = "mammo_processed.csv"
    
    ### Turning Data into numpy array
    my_data = np.genfromtxt(datafilename, delimiter = ",", dtype = str)
    X,Y = my_data[1:,1:-1].astype(float), my_data[1:,-1].astype(float)
    xlabels = my_data[0,1:-1]
    ylabel = [my_data[0,-1]]
    train_ind = list(set(random.sample(range(len(X)), int (.8 * len(X)), )))
    X_train = X[train_ind,:]
    Y_train = Y[train_ind]
    test_ind = [i for i in range(len(X)) if i not in train_ind]
    X_test = X[test_ind, :]
    Y_test = Y[test_ind]



   
    ### Making Slim Class
    ## Optional inputs
    # timelimit  -  number of second for cplex optimization   DEFAULT 300
    # dataset    -  a string name for the dataset for logging purposes DEFAULT: None, sets to CURRENT TIME
    # logging    -  a boolean for whether or not to make a log file in logs
    # verbose    -  a boolean for whether or not to print all the model stuff
    # C0         - determines the accuracy tradeoff we would accept for removing a
                    # coefficient Default: .001 (very low for accuracy, high for simplicity)
    # epsilon    - determines the punishment for a larger total magnitude of coefficients
    # bound      - the upper and lower bound for 
    # logs       - The directory in which a logs directory will be created. This directory must exist 
                #- Default: None, creates a SLIMLogs directory in which logs will be output

    sl = SLIM(dataset = dataset, epsilon = .001, logging = True, 
        time_limit = 50, verbose = True, bound = 5, C0 = .001, logs = None)



    ### CALLING SLIM FUNCTIONS   

    ### ACCEPTS: X, Y, x_labels, ylabel
    ### RETURNS: A STRING VERSION OF THE MODEL
    ## REQUIRED INPUTS
    #X is a numpy array
    #Y is a numpy array with n by 1 dimension
    #xlabels is a list of strings
    #ylabel is a list with 1 string OR a string

    #OPTIONAL INPUT: bin - boolean. If true, all features with 10 or more distinct values will be binned by 
        # mean and deviations off the mean. 0 is the mean, every integer represents the number of standard deviations  
    string_version = sl.fit(X_train,Y_train, xlabels, ylabel, binning = False)
    
    

    ### predict function
    ## ACCEPTS: X  (must have shape as before in second dimension)
    ## RETURNS: A LIST OF PREDICTIONS
    result = sl.predict(X_test)
    print(result)

    ###find accuracy function
    ## ACCEPTS: X   
    ## RETURNS Accuracy - integer
    ##         Confusion - A string with TP, FP, TN, FN
    acc,conf = sl.findAccuracy(result, Y_test)

    ### get_name
    ## returns the name of the model (Rudin-SLIM)
    print(sl.get_name() + " got an accuracy of: " + str(acc) +  ' and a confusion of: ' + conf)



    #FUNCTIONALITY TO ADD:
        #Data scaling
        # Better printouts
        # Simpler importing and Pip package