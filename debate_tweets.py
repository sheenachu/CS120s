import sys
import csv
import os.path
import operator
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tweet_class


# Candidate information (as described in assignment writeup)
CANDIDATE_NAMES = {"bush":      "Jeb Bush",
                   "carson":    "Ben Carson",
                   "christie":  "Chris Christie",
                   "cruz":      "Ted Cruz",
                   "fiorina":   "Carly Fiorina",
                   "gilmore":   "Jim Gilmore",
                   "graham":    "Lindsey Graham",
                   "huckabee":  "Mike Huckabee",
                   "jindal":    "Bobby Jindal",
                   "kasich":    "John Kasich", 
                   "pataki":    "George Pataki",
                   "paul":      "Rand Paul",
                   "perry":     "Rick Perry", 
                   "rubio":     "Marco Rubio", 
                   "santorum":  "Rick Santorum", 
                   "trump":     "Donald Trump", 
                   "walker":    "Scott Walker",
                   "chafee":    "Lincoln Chafee",
                   "clinton":   "Hillary Clinton",
                   "omalley":   "Martin O'Malley",
                   "sanders":   "Bernie Sanders",
                   "webb":      "Jim Webb"}

GOP_CANDIDATES = ['bush', 'carson', 'christie', 'cruz', 'fiorina', 'gilmore', 'graham', 'huckabee', 
                  'jindal', 'kasich', 'pataki', 'paul', 'perry', 'rubio', 'santorum', 'trump', 'walker']

DEM_CANDIDATES = ['chafee', 'clinton', 'omalley', 'sanders', 'webb']

ALL_CANDIDATES = GOP_CANDIDATES + DEM_CANDIDATES


# Size of the figures (these are the values you should pass
# in parameter "figsize" of matplotlib's "figure" function)
# Note: For task 4, use FIGWIDTH*2
FIGWIDTH = 12
FIGHEIGHT = 8


# Start and end time (in seconds) of the debate
DEBATE_START = 86400
DEBATE_END = 97200
# Maximum time (in seconds) of the dataset
MAX_TIME = 183600


# This function generates colors that can be passed to matplotlib functions
# that accept a list of colors. The function takes one parameter: the number
# of colors to generate. Using this function should result in the same colors
# shown in the assignment writeup.
def get_nice_colors(n_colors):
    return cm.Accent( [1 - (i/n_colors) for i in range(n_colors)] )


################################################
#
# Your functions go here
#
# Call your functions from the __main__ block
#
################################################

def create_tweets_from_file(filename):
    '''
    Function takes a CSV file and returns a list of tweets
    '''
    with open(filename, 'r') as f:
        tweet_dict = csv.DictReader(f)
        rv = [tweet_class.Tweet(t['seconds'], t['candidates']) for t in tweet_dict]
        return rv

def num_candidates_mentioned_vs_num_tweets_data(tweets):
    rv = {}

    for tweet in tweets:
        num_candidates = len(tweets.candidates)
        rv[num_candidates] = rv.get(num_candidates, 0) + 1

    return rv

def top_paired_candidates(tweets, candidate_list):
    pair_frequency = {}
    rv = []
    for tweet in tweets:
        for i in tweet.candidates:
            for j in tweet.candidates:
                if j > i:
                    if (i + j) in pair_frequency:
                        pair_frequency[i + j] += 1
                    elif (j + i) in pair_frequency:
                        pair_frequency[j + i] += 1
                    else:
                        pair_frequency[(i + j)] = 1

    for pair in pair_frequency:
        rv.append(pair, pair_frequency[pair])

    return rv.sort[0:10]

def bar(x,y):
    n_groups = len(x) + 1

    data = y

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

    plt.show()

def pie():
    plt.figure(1, figsize=(6,6))
    ax = plt.axes([0.1, 0.1, 0.8, 0.8])

    labels = ['Frogs', 'Hogs', 'Dogs', 'Logs'] #list of names of candidates
    fracs = [15, 30, 45, 10] #percentage of mentions 

    plt.pie(fracs, labels=labels,
                autopct='%1.1f%%', startangle=0)

    plt.title('Raining Hogs and Dogs')

    plt.show()

'''
if __name__ == "__main__":

    # The following code parses the command-line parameters. 
    # There is one required parameter (the CSV file) and an optional
    # parameter (the directory where the PNG files will be created;
    # if not specified, this defaults to "output/").
    #
    # This code results in two variables:
    #
    #  - csv_file: The data file to read
    #  - output_dir: The directory where the images should be generated

    if not 2 <= len(sys.argv) <= 3:
        print("Usage: python3 {} <data file> [<output directory>]".format(sys.argv[0]))
        sys.exit(1)
    else:
        csv_file = sys.argv[1]
        if not os.path.exists(csv_file) or not os.path.isfile(csv_file):
            print("{} does not exist or is not a file.".format(csv_file))
            sys.exit(1)
        if len(sys.argv) == 3:
            output_dir = sys.argv[2]
            if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
                print("{} does not exist or is not a directory.".format(output_dir))
                sys.exit(1)
        else:
            output_dir = "./output"

    # Use the following file names to generate the plots
    TASK1_FILE = "{}/bar_num_mentions.png".format(output_dir)

    TASK2_GOP_FILE = "{}/bar_candidates_together_gop.png".format(output_dir)
    TASK2_ALL_FILE = "{}/bar_candidates_together_all.png".format(output_dir)

    TASK3_GOP_FILE = "{}/candidates_gop.png".format(output_dir)
    TASK3_ALL_FILE = "{}/candidates_all.png".format(output_dir)

    TASK4A_DURING_FILE = "{}/mentions_over_time_during.png".format(output_dir)
    TASK4A_FULL_FILE = "{}/mentions_over_time.png".format(output_dir)

    TASK4B_FILE = "{}/stackplot.png".format(output_dir)


    # Your code goes here, BUT NOT **ALL** YOUR CODE.
    #
    # You should write functions that do all the work, and then
    # call them from here.

def bar_num_mentions():
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
'''