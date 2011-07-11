from zope.interface import Attribute, Interface


class IBallotBox(Interface):
    """
    """
    method = Attribute("The voting method used")

    def addVote(self, vote):
        """
        Add a single vote at a time.

        Depending upon the voting method, the data type of the passed parameter
        'vote' could change.
        """

    def addVotes(self, votes):
        """
        Add multiple votes at a time.
        """

    def countVotes(self):
        """
        Generate a tally of votes.
        """
