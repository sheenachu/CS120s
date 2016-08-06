# ESTELLE OSTRO & SHEENA CHU
# PROGRAMMING ASSIGNMENT 4
# Voter Sample Class

import random
import voter

class VoterSample(object):


    def __init__(self, num_voters, minutes_open, voting_mean):
        self.num_voters = num_voters
        self.minutes_open = minutes_open
        self.voting_mean = voting_mean
        self.voters = self.list_sample()
        self.nvoters = len(self.voters)

    def list_sample(self):
        lambd = (self.num_voters / self.minutes_open)
        t_arrival = 0
        voter_sample = []
        for i in range(self.num_voters):
            gap = random.expovariate(lambd)
            t_arrival += gap
            t_vote = random.expovariate(1 / self.voting_mean)
            voter_sample.append(voter.Voter(t_arrival, t_vote))
            
            if t_arrival > self.minutes_open:
                voter_sample.pop()
                break

        return voter_sample

    def has_next(self):
        return len(self.voters) > 0

    def next(self):
        return self.voters.pop(0)

    def __repr__(self):
        return str(self.voters)

