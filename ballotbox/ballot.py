from zope.interface import implements

from ballotbox.iballot import IBallotBox


class BallotBox(dict):
    """
    """
    implements(IBallotBox)
    
    def __init__(self, method=None, *args, **kwargs):
        super(BallotBox, self).__init__(*args, **kwargs)
        # instantiate the voting method class
        if method:
            #import pdb;pdb.set_trace()
            method = method()
        self.method = method

    def add_vote(self, vote):
        self.update(vote)

    def add_votes(self, votes):
        self.update(votes)

    def get_total_votes(self):
        return sum(self.values())

    def get_winner(self, *args, **kwargs):
        return self.method.get_winner(self, *args, **kwargs)
