# CS 122 W'16: Clean Pima Indians Diabetes Data
#
# ESTELLE OSTRO & SHEENA CHU

import csv
import random
import sys
import pandas as pd
import numpy as np

ELIMINATE = [" Plasma glucose level", " Diastolic Blood Pressure",
            " Triceps skin foldthickness", " 2-Hour serum insulin (mu U/ml)", " Body Mass Index"]

CONVERT_DICT = {("Pregnant", "Number of pregnancies"): [("low", 0, 2), ("medium", 2, 6), ("high", 6, float('inf'))],
    ("Plasma glucose"," Plasma glucose level"): [("low", 0.1, 95), ("medium", 95, 141), ("high", 141, float('inf'))],
    ("Diastolic blood pressure", " Diastolic Blood Pressure"): [("normal", 0.1, 80), ("pre-hypertension", 80, 90),
                                                                ("high", 90, float('inf'))],
    ("Body mass index", " Body Mass Index"): [("low", 0.1, 18.5), ("healthy", 18.5, 25.1), ("overweight", 25.1, 30.1),
                                            ("obese", 30.1, 35.1), ("severely-obese", 35.1, float('inf'))],
    ("Diabetes pedigree function", " Diabetes Pedigree Function"): [("low", 0.1, 0.42), ("medium", 0.42, 0.82), ("high", 0.82, float('inf'))],
    ("Age", " Age (in years)"):[("r1", 0.1, 41), ("r2", 41, 60), ("r3", 60, float('inf'))]}


def clean(raw_filename):
    raw = pd.read_csv(raw_filename)
    x = raw.groupby(ELIMINATE).groups
    empty = []

    for key in x.keys():
        if 0 in key:
            empty.append(x[key][0])

    cleaned = raw.drop(raw.index[empty]).reset_index()
    del cleaned['index']

    return cleaned

def convert(raw_filename):
    cleaned = clean(raw_filename)
    below = []

    del cleaned[" Triceps skin foldthickness"]
    del cleaned[" 2-Hour serum insulin (mu U/ml)"]

    for i in range(len(cleaned)):
        for k in CONVERT_DICT.keys():
            for l in range(len(CONVERT_DICT[k])):
                if CONVERT_DICT[k][l][1] <= cleaned[k[1]][i] < CONVERT_DICT[k][l][2]:
                    cleaned.ix[i, k[1]] = CONVERT_DICT[k][l][0]
                    break
                elif cleaned[k[1]][i] < CONVERT_DICT[k][0][1]:
                    below.append(i)
                    break
    
    if below:
        converted = cleaned.drop(cleaned.index[below]).reset_index()
        del converted["index"]
        return converted


    return cleaned


def go(raw_filename, training_filename, testing_filename):
    
    df = convert(raw_filename)
    msk = np.random.rand(len(df)) < 0.9
    train = df[msk]
    test = df[~msk]

    train = train.to_csv(training_filename, index = False)
    test = test.to_csv(testing_filename, index = False)


if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: python3 {} <raw data filename> <training filename> <testing filename>".format(sys.argv[0]))
        sys.exit(1)

    go(sys.argv[1], sys.argv[2], sys.argv[3])