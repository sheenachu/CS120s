# ESTELLE OSTRO & SHEENA CHU
# PROGRAMMING ASSIGNMENT 4
# Precinct Class

import queue

class Precinct(object):
    def __init__(self, number_of_booths):
        self.number_of_booths = number_of_booths
        self.booths = queue.PriorityQueue(self.number_of_booths)

    def add_voter(self, voter):
        assert not self.is_full()
        return self.booths.put((voter.t_depart, voter))

    def remove_voter(self):
        assert not self.is_empty()
        return self.booths.get()

    def is_full(self):
        return self.booths.full()

    def is_empty(self):
        return self.booths.empty()


