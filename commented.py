# CS121 A'15: Polling places
#
# ESTELLE OSTRO & SHEENA CHU
#
# Main file for polling place simulation


import json
import math
import os
import random
import sys
import time
import voter_sample
import precinct



def simulate_election_day(params):
    '''
    Simulate a single election day.

    Input:
        params: configuration to simulate

    Output:
        True if the specified configruation was suffient to meet the
        threshold for one simulated election day, false otherwise.
   
    '''
    
    vs = voter_sample.VoterSample(params['num_voters'], 
            params['hours_open']*60, params['voting_mean'])

    p = precinct.Precinct(params['number_of_booths'])

    counts = 0

    #while there are still voters in the sample
    while vs.has_next():
        v = vs.next()
        #if the voting booths aren't full. t_assign = t_arrival                 
        if not p.is_full():
            v.t_assign = v.t_arrival
            v.t_depart = v.t_assign + v.t_vote
            p.add_voter(v)
        #if the voting booths are full
        else:
            #skip to time where first voter departs
            t = p.remove_voter()[0]
            #if time of voter depart is before voter arrives. assign upon arrival
            if t < v.t_arrival:
                v.t_assign = v.t_arrival
            #if voter depart is after voter arrives, assign at time voter departs
            else:
                v.t_assign = t
            v.t_depart = v.t_assign + v.t_vote                                           
            #if wait time is greater than threshold add one to counts
            if v.wait > params['target_waiting_time']:
                counts += 1 
            p.add_voter(v)                          

    return (counts / vs.nvoters)*100 < params['threshold']


def run_trials(params):
    '''
    Run trials on the configuration specified by the parameters file.

    Inputs: 
        params: simulation parameters
    
    Result:
        Likelihood that the given number of machines is sufficient for
        the specified configuration.
    '''
    count = 0.0
    for t in range(params["num_trials"]):
        if simulate_election_day(params):
            count = count + 1.0
    
    return count/params["num_trials"]


def setup_params(params_filename, num_booths):
    '''
    Set up the paramaters data structure and set the
    seed for the random number generator

    Inputs:
        params_filename: name of the simulation parameters file
        num_booths: the number of booths to simulate
    '''
    if not os.path.isfile(params_filename):
        print("Error: cannot open parameters file " + params_filename)
        sys.exit(0)

    if num_booths <= 0:
        print("Error: the number of voting booths must be positive")
        sys.exit(0)

    params = json.load(open(params_filename))
    params["number_of_booths"] = num_booths

    if "seed" in params:
        seed = params["seed"]
    else:
        seed = int(time.time())
        params["seed"] = seed

    random.seed(seed)

    return params


if __name__ == "__main__":
    usage_str = "usage: python {0} [parameters filename] [number of voting booths]".format(sys.argv[0])
    # process arguments
    num_booths = 8
    params_filename = "data/params2.json"
    if len(sys.argv) == 2:
        params_filename = sys.argv[1]
    elif len(sys.argv) == 3:
        params_filename = sys.argv[1]
        num_booths = int(sys.argv[2])
    elif len(sys.argv) > 3:
        print(usage_str)
        sys.exit(0)

    params = setup_params(params_filename, num_booths)
    rv = run_trials(params)

    # print the parameters and the result
    for key in sorted(params):
        print(key + ": " + str(params[key]))
    print()
    print("result: " + str(rv))