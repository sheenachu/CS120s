class Tweet(object):

    def __init__(self, seconds, candidates):
        '''
        Constructor
        '''
        self.candidates = candidates.split('|')
        self.seconds = seconds

    def seconds(self):
        return self._seconds

    def candidates(self):
        return self._candidates

    def __repr__(self):
        return '({}, {})'.format(self.seconds, ', '.join(self.candidates))

