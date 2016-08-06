import numpy as np
import matplotlib.pyplot as plt

#####################
#   BAR GRAPH!!!    #
#####################
def bar():
    n_groups = 10 #len(candidates) + 1

    data = (1,2,3,4,5,100, 1000, 10000, 100000, 200) #number of tweets per mention

    #fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.9

    bars = plt.bar(index, data, bar_width,
                     color='blue',
                     label='Men')

    plt.xlabel('Number of Mentions')
    plt.ylabel('Number of Tweets')
    plt.title('Number of Candidate Mentions per Tweet')
    plt.xticks(index + 0.5*bar_width, range(len(index)+1)) #len(candidates)
    plt.yscale('log', nonposy='clip')

    #plt.tight_layout()
    plt.show()


#####################
#   PIE CHART!!!    #
#####################

# make a square figure and axes
def pie():
    plt.figure(1, figsize=(6,6))
    ax = plt.axes([0.1, 0.1, 0.8, 0.8])

    labels = ['Frogs', 'Hogs', 'Dogs', 'Logs'] #list of names of candidates
    fracs = [15, 30, 45, 10] #percentage of mentions 

    plt.pie(fracs, labels=labels,
                autopct='%1.1f%%', startangle=0)

    plt.title('Raining Hogs and Dogs')

    plt.show()