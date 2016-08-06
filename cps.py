# CS121 A'15: Current Population Survey (CPS) 
#
# Functions for mining CPS data 
#
# Sheena Chu

from pa3_helpers import read_csv, plot_histogram
import numpy as np

# Constants 
HID = "h_id" 
AGE = "age"
GENDER = "gender" 
RACE = "race" 
ETHNIC = "ethnicity" 
STATUS = "employment_status"
HRWKE = "hours_worked_per_week" 
EARNWKE = "earnings_per_week" 

FULLTIME_MIN_WORKHRS = 35

COLUMN_WIDTH = 18
COLUMN_SEP = "|"

MEAN_INDEX = 0
MEDIAN_INDEX = 1
MIN_INDEX = 2
MAX_INDEX = 3

def build_morg_dict(input_dict):
    '''
    Build a dictionary that holds a set of CPS data 

    Inputs:
        input_dict: dict

        An example of input_dict is shown below: 
        {'morg':'data/morg_d14_mini.csv',
         'gender_codes':'data/gender_code.csv',
         'race_codes':'data/race_code.csv',
         'ethnic_codes':'data/ethnic_code.csv',
         'employment_codes':'data/employment_status_code.csv'}

    Returns:
        dict 

    return {} 
    '''
    inputs = {}
    codes = {}
    morg_dict = {}
    keys = [AGE, GENDER, RACE, ETHNIC, STATUS, HRWKE, EARNWKE]

    for i in input_dict:
        inputs[i] = read_csv(input_dict[i], False)

    for i in inputs:
        if i != 'morg':
            codes[i] = {}
            for j in inputs[i]:
                codes[i].update({j[0] : j[1]})
            codes[i].update({'' : ''})
            continue  

    gender = codes['gender_codes']
    race = codes['race_codes']
    ethnic = codes['ethnic_codes']
    ethnic.update({'':'Non-Hispanic'})
    employ = codes['employment_codes']

    for i in inputs['morg']:
        d = {}
        for j in range(len(keys)):
            d[keys[j]] = i[j + 1]
        d[AGE] = int(d[AGE])
        d[GENDER] =  gender[d[GENDER]]
        d[RACE] = race[d[RACE]]
        d[ETHNIC] = ethnic[d[ETHNIC]]
        d[STATUS] = employ[d[STATUS]]
        if d[HRWKE] != '':
            d[HRWKE] = int(d[HRWKE])
        if d[EARNWKE] != '':
            d[EARNWKE] = float(d[EARNWKE])
        morg_dict[i[0]] = d
 
    return morg_dict

def create_histogram(morg_dict, var_of_interest, num_buckets, 
                     min_val, max_val):
    '''
    Create a histogram using a list 

    Inputs:
        morg_dict: a MORG dictionary 
        var_of_interest: string (e.g., HRWKE or EARNWKE)
        num_buckets: number of buckets in the histogram
        min_val: the minimal value (lower bound) of the histogram
        max_val: the maximal value (upper bound) of the histogram 

    Returns:
        list that represents a histogram 
    '''

    if num_buckets == 0:
        hist = []
        return hist

    hist = [0] * num_buckets
    len_buckets = (max_val - min_val) / num_buckets
    width = ((max_val - min_val) / (num_buckets))
        
    for i in range(num_buckets):
        for j in morg_dict:
            if (morg_dict[j][STATUS] == 'Working'
                and morg_dict[j][HRWKE] >= FULLTIME_MIN_WORKHRS
                and (i * width + min_val) <=
                morg_dict[j][var_of_interest] < ((i + 1) * (width) + min_val)):
                    hist[i] = hist[i] + 1
    return hist

def calc_rate(morg_d, var_of_interest, age_range):
    '''
    Inputs:
        morg_d: dictionary
        var_of_interest: string
        age_range: tuple of two integers

    Function takes a dictionary, variable of interest, and age range
    and returns a dictionary containing unemployement rates.

    Returns:
        rate: dictionary of unemployment rates
    '''
    unemploy = {}
    total = {}
    rate = {}

    for i in morg_d:
        if age_range[0] <= morg_d[i][AGE] <= age_range[1]:
            if (morg_d[i][STATUS] == "Layoff") or (morg_d[i][STATUS] == "Looking"):
                if morg_d[i][var_of_interest] not in unemploy:
                    unemploy[morg_d[i][var_of_interest]] = 0
                unemploy[morg_d[i][var_of_interest]] += 1
            if (morg_d[i][STATUS] == "Layoff" 
                or morg_d[i][STATUS] ==  "Working" 
                or morg_d[i][STATUS] ==  "Looking"):
                    if morg_d[i][var_of_interest] not in total:
                        total[morg_d[i][var_of_interest]] = 0
                    total[morg_d[i][var_of_interest]] += 1

    for j in total:
        if j in unemploy: 
            rate.update({j : (unemploy[j] / total[j])})
        else:
            rate.update({j : 0.00})

    return rate


def build_table(year_d, var_of_interest):
    '''
    Function builds a table of unemployment rates.

    Inputs:
        year_dict: dict whose keys are years and values are 
                    unemployment rates
        var_of_interest: string

    Returns:
        table: list
    '''
    num_col = len(year_d) + 1
    year = sorted(year_d)

    table = [(COLUMN_SEP + ('{:<{}}'.format('Year', COLUMN_WIDTH) 
            + COLUMN_SEP))]
    
    for y in year:
        table[0] += ('{:<{}.{}}'.format(y, COLUMN_WIDTH, COLUMN_WIDTH)
                    + COLUMN_SEP)

    codes = {ETHNIC : read_csv('data/ethnic_code.csv', False), 
            GENDER : read_csv('data/gender_code.csv', False), 
            RACE : read_csv('data/race_code.csv', False)}
    var = {}

    for i in codes:
        var[i] = []
        for j in codes[i]:
            var[i].append(j[1])
            var[i].sort()

    for j in var[var_of_interest]:
        row = COLUMN_SEP + ('{:<{}.{}}'.format(j, COLUMN_WIDTH, COLUMN_WIDTH)
                    + COLUMN_SEP) 
        for i in year:
            if j in year_d[i]:
                row += ('{:<{}.2f}'.format(year_d[i][j], COLUMN_WIDTH) 
                    + COLUMN_SEP)
            else:
                row += ('{:<{}.2f}'.format(0.00, COLUMN_WIDTH) 
                    + COLUMN_SEP)
        table.append(row)

    return table


def calculate_unemployment_rates(filename_list, age_range, var_of_interest):
    '''
    Output a nicely formatted table for the unemployment rates 
    for the specified age_rage, 
    further broken down by different categories in var_of_interest
    for the data specified in each file in filename_list 

    Inputs:
        filename_list: a list of MORG dataset file names
        age_rage: a tuple consisted of two integers
        var_of_interest: string (e.g., AGE, RACE or ETHNIC)

    Returns:
        list 
    '''
    unemploy_table = []
    input_dict = {'gender_codes':'data/gender_code.csv',
         'race_codes':'data/race_code.csv',
         'ethnic_codes':'data/ethnic_code.csv',
         'employment_codes':'data/employment_status_code.csv'}

    if filename_list == []:
        return []
    filename_list = list(set(filename_list))

    year_d = {}
    for f in filename_list:
        input_dict.update({'morg' : 'data/{}'.format(f)})
        morg_d = build_morg_dict(input_dict)
        rate = calc_rate(morg_d, var_of_interest, age_range)
        year_d.update({f[6:8] : rate})

    unemploy_table = build_table(year_d, var_of_interest)

    return unemploy_table

def calculate_unemployment_rates(filename_list, age_range, var_of_interest):
    '''
    Output a nicely formatted table for the unemployment rates 
    for the specified age_rage, 
    further broken down by different categories in var_of_interest
    for the data specified in each file in filename_list 

    Inputs:
        filename_list: a list of MORG dataset file names
        age_rage: a tuple consisted of two integers
        var_of_interest: string (e.g., AGE, RACE or ETHNIC)

    Returns:
        list 
    '''
    unemploy_table = []
    input_dict = {'gender_codes':'data/gender_code.csv',
         'race_codes':'data/race_code.csv',
         'ethnic_codes':'data/ethnic_code.csv',
         'employment_codes':'data/employment_status_code.csv'}

    if filename_list == []:
        return []
    filename_list = list(set(filename_list))

    year_d = {}
    for f in filename_list:
        input_dict.update({'morg' : 'data/{}'.format(f)})
        morg_dict = build_morg_dict(input_dict)
        rate = calc_rate(morg_dict, var_of_interest, age_range)
        year_d.update({f[6:8] : rate})

    unemploy_table = build_table(year_d, var_of_interest)


    return unemploy_table 

def calculate_weekly_earnings_stats_for_fulltime_workers(morg_dict, gender, 
                                                         race, ethnicity):
    '''
    Returns a 4-element list of earnings statics (mean, median, min, and max) 
    for all fulltime workers who satisfy the given query criteria 

    Inputs:
        morg_dict: dict 
        gender: query criteria for gender 
        race: query criteria for race 
        ethnicity: query criteria for ethnicity 

    Returns:
        A 4-element list
    '''

    codes = {ETHNIC : read_csv('data/ethnic_code.csv', False), 
            GENDER : read_csv('data/gender_code.csv', False), 
            RACE : read_csv('data/race_code.csv', False)}

    if gender == "All":
        gender = ("Male" or "Female")
    if race == "Other":
        race = []
        for i in range(5,26):
            race_code = codes[RACE][i][1]
            race.append(race_code)
        print(race)
    if race == "All":
        race = []
        for i in range(0,26):
            race_code = codes[RACE][i][1]
            race.append(race_code)
    if ethnicity == "Hispanic":
        ethnicity = []
        for i in range(1,9):
            ethnic = codes[ETHNIC][i][1]
            ethnicity.append(ethnic)
    if ethnicity == "All":
        ethnicity = []
        for i in range(0,9):
            ethnic = codes[ETHNIC][i][1]
            ethnicity.append(ethnic)

    all_values = []
    stats = [0]*4
    
    for i in morg_dict:
        if (morg_dict[i][GENDER] == gender
            and morg_dict[i][RACE] in race
            and morg_dict[i][ETHNIC] in ethnicity
            and morg_dict[i][STATUS] == 'Working'
            and morg_dict[i][HRWKE] >= FULLTIME_MIN_WORKHRS):
                earned = morg_dict[i][EARNWKE]
                all_values.append(earned)

    if all_values == []:
        return stats
    
    all_values = sorted(all_values)
    mean = np.mean(all_values)
    median = np.median(all_values)
    min_val = min(all_values)
    max_val = max(all_values)

    stats[MEAN_INDEX] = mean
    stats[MEDIAN_INDEX] = median
    stats[MIN_INDEX] = min_val
    stats[MAX_INDEX] = max_val

    return stats