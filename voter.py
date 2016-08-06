# ESTELLE OSTRO & SHEENA CHU
# PROGRAMMING ASSIGNMENT 4
# Voter Class

class Voter(object):
    VOTER_ID = 0

    def __init__(self, t_arrival, t_vote):
        Voter.VOTER_ID += 1
        self.vid = Voter.VOTER_ID
        self.t_arrival = t_arrival
        self.t_vote = t_vote
        self.t_assign = None
        self.t_depart = None

    @property
    def wait(self):
        if self.t_assign == None:
            return None
        else:
            return self.t_assign-self.t_arrival

    def __str__(self):
        return "Voter({}, {}, {})".format(self.vid, self.t_arrival, self.t_vote)

    def __repr__(self):
        return str(self)    
        