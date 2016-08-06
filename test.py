# CS122 W'16: Markov models and hash tables
# SHEENA CHU 

import sys
import math
import Hash_Table

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        self.k = k
        self.string = s
        ht = Hash_Table.Hash_Table(HASH_CELLS, False)
        for i in range(len(self.string)):
            key1, key2 = self.create_key(s,k,i)
            value1 = ht.lookup(key1)
            value2 = ht.lookup(key2)
            if not value1:
                ht.update(key1,1)
            else:
                ht.update(key1,(value1 + 1))
            if not value2:
                ht.update(key2,1)
            else:
                ht.update(key2, (value2 + 1))
        self.hashtable = ht

    def create_key(self,s,k,i):
        '''
        
        '''

        if i < k:
            key1 = s[-(k-i):] + s[0:i]
            key2 = key1 + s[i]

        else:
            key1 = s[i-k:i]
            key2 = key1 + s[i]
        return key1, key2


    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        '''
        S = len(set(self.string))
        k = self.k
        probability = 0
        for i in range(len(s)):
            key1, key2 = self.create_key(s, k, i)
            N = self.hashtable.lookup(key1)
            M = self.hashtable.lookup(key2)
            if not N:
                N = 0
            if not M:
                M = 0
            P = (M + 1)/(N + S)
            probability += math.log(P)
        return probability


def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the normalized log probabilities of each of the speakers
    uttering that text under a "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    m1 = Markov(order, speech1)
    m2 = Markov(order, speech2)
    p1 = m1.log_probability(speech3)/len(speech3)
    p2 = m2.log_probability(speech3)/len(speech3)
    if p1 > p2:
        conclusion = 'A'
    else:
        conclusion = 'B'

    return (str(p1),str(p2), conclusion)

def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")

if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)
