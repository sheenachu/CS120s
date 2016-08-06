# CS 122 W'16: Building decision trees
#
# Your name(s)

import csv
import math
import sys

def read_csv(filename):
    rv = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rv.append(row)
    attr = rv[0]
    rv = rv[1:]
    return attr, rv

def attribute_dict(observations):
    '''
    observations: list of dictionaries
    '''
    rd = {}
    for o in observations:
        for i in range(len(o)):
            rd[i] = rd.get(i, [o[i]])
            if o[i] not in rd[i]:
                rd[i].append(o[i])
    return rd

class DecisionTree:
    def __init__(self, observations, target, attribute_dict):
        '''
        Creates a new decision tree node.
        '''
        self.children = {}
        self.obs = observations
        self.t = target
        self.attr_dict = attribute_dict
        self.split_attr = None
        self.edge = None
        self.cls = self.argmax()

    def argmax(self):
        rv = (None, 0)
        for o in self.obs:
            attr = range(len(o)-1)
            value = o[self.t]
            for a in attr:
                subset = self.value_subset(a, value)
                frac = self.attribute_fraction(subset)
                if frac > rv[1]:
                    rv = (value, frac)
                    print(o, rv)
        return rv[0]

    def value_subset(self, attribute, value):
        rv = []
        for o in self.obs:
            if o[attribute] == value:
                rv.append(o)
        return rv

    def attribute_fraction(self, subset):
        '''
        observations: list of dict
        subset: list of dict
        value: str
        '''
        rv = len(subset) / len(self.obs)
        return rv

    def split(self, obs, value, t, attr):
        self.children[self.cls] = DecisionTree(obs, value, t, attr)

def gini(observations, attribute, attribute_dict):
    total = 0
    for value in attribute_dict[attribute]:
        subset = value_subset(observations, attribute, value)
        total += (attribute_fraction(observations, subset))**2
    rv = 1 - total
    return rv

def gain(observations, attribute, target, attribute_dict):
    total = 0
    for value in attribute_dict[attribute]:
        subset = value_subset(observations, attribute, value)
        total += (attribute_fraction(observations, subset) * 
                    gini(subset, target, attribute_dict))
    rv = gini(observations, target, attribute_dict) - total
    return rv

def split_info(observations, attribute, attribute_dict):
    total = 0
    for value in attribute_dict[attribute]:
        subset = value_subset(observations, attribute, value)
        total += (attribute_fraction(observations, subset) * 
                    math.log(attribute_fraction(observations, subset)))
    rv = -total
    return rv

def gain_ratio(observations, attribute, target, attribute_dict):
    g = gain(observations, attribute, target, attribute_dict)
    s_i = split_info(observations, attribute, attribute_dict)
    rv = g / s_i
    return rv

def max_gain_value(observations, attribute_dict):
    rv = (None, 0)
    for o in observations:
        attr = o[:-1]
        t = o[-1]
        for a in attr:
            gain = gain_ratio(observations, a, t, attribute_dict)
            if gain > rv[1]:
                rv = (index(a), gain)
    return rv[0]

def create_decision_tree(observations, attribute, target, attribute_dict):
    #base case
    # node = DecisionTree(observations, target, attribute_dict)
    # for o in observations:
    #     if o[attribute] != node.cls:
    #         break
    # recursive case
        node.split_attr = max_gain_value(observations, attribute_dict)
        value = node.split_attr
        obs = value_subset(observations, attribute, value)
        t = len(obs[0])-1
        attr = attribute_dict(obs)
        create_decision_tree(obs, value, t, attr)

def go(training_filename, testing_filename):
    # replace return with a suitable return value
    # and remove this comment!
    return []


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("usage: python3 {} <training filename> <testing filename>".format(sys.argv[0]))
        sys.exit(1)

    for result in go(sys.argv[1], sys.argv[2]):
        print(result)
