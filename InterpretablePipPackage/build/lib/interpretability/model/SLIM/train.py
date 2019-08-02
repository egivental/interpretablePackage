import sys
import os
import numpy as np
import pandas as pd
import cplex as cp
import subprocess
from .slim import SLIMCoefficientConstraints, create_slim_IP, get_slim_summary, check_data, check_slim_IP_output

#### LOAD DATA ####
# requirements for CSV data file
# - outcome variable in first column
# - outcome variable values should be [-1, 1] or [0, 1]
# - first row contains names for the outcome variable + input variables
# - no empty cells

def main(data, timelimit, bound, c0, epsilon) :
    #data_dir = os.getcwd() + '/slim-python-master/data/'
    #data_csv_file = data_dir + data_name + '_processed.csv'

    # load df file from csv
    #print(data_csv_file)
    #df = pd.read_csv(data_csv_file, sep = ',')
    
    data_headers = np.array(data)[0,:]
    data = np.array(data[1:,:], dtype = "int64")
    N = data.shape[0]


    # setup Y vector and Y_name
    Y_col_idx = [0]
    Y = data[:, Y_col_idx]
    Y_name = [data_headers[j] for j in Y_col_idx]
    Y[Y == 0] = -1

    # setup X and X_names
    X_col_idx = [j for j in range(data.shape[1]) if j not in Y_col_idx]
    X = data[:, X_col_idx]
    X_names = [data_headers[j] for j in X_col_idx]

    # insert a column of ones to X for the intercept
    X = np.insert(arr = X, obj = 0, values = np.ones(N), axis = 1)
    X_names.insert(0, '(Intercept)')

    # run sanity checks
    check_data(X = X, Y = Y, X_names = X_names)

    #### TRAIN SCORING SYSTEM USING SLIM ####
    # setup SLIM coefficient set
    coef_constraints = SLIMCoefficientConstraints(variable_names = X_names, ub = bound, lb = -bound)
    coef_constraints.view()

    #choose upper and lower bounds for the intercept coefficient
    #to ensure that there will be no regularization due to the intercept, choose
    #
    #intercept_ub < min_i(min_score_i)
    #intercept_lb > max_i(max_score_i)
    #
    #where min_score_i = min((Y*X) * \rho) for rho in \Lset
    #where max_score_i = max((Y*X) * \rho) for rho in \Lset
    #
    #setting intercept_ub and intercept_lb in this way ensures that we can always
    # classify every point as positive and negative
    scores_at_ub = (Y * X) * coef_constraints.ub
    scores_at_lb = (Y * X) * coef_constraints.lb
    non_intercept_ind = np.array([n != '(Intercept)' for n in X_names])
    scores_at_ub = scores_at_ub[:, non_intercept_ind]
    scores_at_lb = scores_at_lb[:, non_intercept_ind]
    max_scores = np.fmax(scores_at_ub, scores_at_lb)
    min_scores = np.fmin(scores_at_ub, scores_at_lb)
    max_scores = np.sum(max_scores, 1)
    min_scores = np.sum(min_scores, 1)

    intercept_ub = -min(min_scores) + 1
    intercept_lb = -max(max_scores) + 1
    coef_constraints.set_field('ub', '(Intercept)', intercept_ub)
    coef_constraints.set_field('lb', '(Intercept)', intercept_lb)
    coef_constraints.view()


    #create SLIM IP
    slim_input = {
        'X': X,
        'X_names': X_names,
        'Y': Y,
        'C_0': c0,
        'w_pos': 1.0,
        'w_neg': 1.0,
        'L0_min': 0,
        'L0_max': float('inf'),
        'err_min': 0,
        'err_max': 1.0,
        'pos_err_min': 0,
        'pos_err_max': 1.0,
        'neg_err_min': 0,
        'neg_err_max': 1.0,
        'coef_constraints': coef_constraints
    }

    slim_IP, slim_info = create_slim_IP(slim_input, epsilon)

    # setup SLIM IP parameters
    # see docs/usrccplex.pdf for more about these parameters
    slim_IP.parameters.timelimit.set(timelimit) #set runtime here
    #TODO: add these default settings to create_slim_IP
    slim_IP.parameters.randomseed.set(0)
    slim_IP.parameters.threads.set(1)
    slim_IP.parameters.parallel.set(1)
    slim_IP.parameters.output.clonelog.set(0)
    slim_IP.parameters.mip.tolerances.mipgap.set(np.finfo(np.float).eps)
    slim_IP.parameters.mip.tolerances.absmipgap.set(np.finfo(np.float).eps)
    slim_IP.parameters.mip.tolerances.integrality.set(np.finfo(np.float).eps)
    slim_IP.parameters.emphasis.mip.set(1)


    # solve SLIM IP
    slim_IP.solve()

    # run quick and dirty tests to make sure that IP output is correct
    check_slim_IP_output(slim_IP, slim_info, X, Y, coef_constraints)

    #### CHECK RESULTS ####
    slim_results = get_slim_summary(slim_IP, slim_info, X, Y)
    #print(slim_results)

    # print model
    string = slim_results['string_model']

    # print coefficient vector
    

    # print accuracy metrics
    #print ('error_rate: %1.2f%%' % (100*slim_results['error_rate']))
    #print ('TPR: %1.2f%%' % (100*slim_results['true_positive_rate']))
    #print ('FPR: %1.2f%%' % (100*slim_results['false_positive_rate']))
    #print ('true_positives: %d' % slim_results['true_positives'])
    #print ('false_positives: %d' % slim_results['false_positives'])
    #print ('true_negatives: %d' % slim_results['true_negatives'])
    #print ('false_negatives: %d' % slim_results['false_negatives'])
    #print(slim_results['rho'])
    return string, slim_results['rho']



if __name__ == '__main__':  
    datafileName = sys.argv[1]
    main(datafileName)


