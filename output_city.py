# CS121 Linear regression assignment
# 
# SHEENA CHU (sheenachu)
#
# Generate plots and print text answers for the CITY data
#
import sys
from model import (linear_regression, apply_beta, read_file,
                    create_model, r_squared, task_1, task_2,
                    sim_k, task_3a, task_3b, task_4)

# useful defined constants for the city data
COMPLAINT_COLS = range(0, 7)
CRIME_TOTAL_COL = 7


if __name__ == "__main__":
     
    predictors = COMPLAINT_COLS
    dependent = CRIME_TOTAL_COL

    model = create_model('city', dependent, predictors, training = True)
    training_model = create_model('city', dependent, predictors, training = True)
    testing_model = create_model('city', dependent, predictors, training = False)

    task_1(model)
    task_2(model)
    task_3a(model)
    task_3b(model, 0.1)
    task_3b(model, 0.01)
    task_4(training_model, testing_model)