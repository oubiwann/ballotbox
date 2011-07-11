from zope.interface import implements

from ballotbox.iballotbox import IBallotBox


class BallotBox(dict):
    """
    """
    implements(IBallotBox)
    
    def __init__(self, method=None, *args, **kwargs):
        super(BallotBox, self).__init__(*args, **kwargs)
        # instantiate the voting method class
        self.method = method()

    def addVote(self, vote):
        pass

    def addVotes(self, votes):
        pass

    def countVotes(self):
        pass
