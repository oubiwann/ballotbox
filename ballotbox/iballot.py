from zope.interface import Attribute, Interface


class IBallotBox(Interface):
    """
    """
    method = Attribute("The voting method used")

    def add_vote(self, vote):
        """
        Add a single vote at a time.

        Depending upon the voting method, the data type of the passed parameter
        'vote' could change.
        """

    def add_votes(self, votes):
        """
        Add multiple votes at a time.
        """

    def get_total_votes(self):
        """
        Count all otes cast for all candidates.
        """

    def get_winner(self):
        """
        Determine the winner, if one exists.

        This is a wrapper for the mehtod of the same name on the IVotingMethod
        implementation class.
        """


class IVotingMethod(Interface):
    """
    """
    def get_winner(self, ballotbox):
        """
        For the sake of consistency between voting methods, get_winner should
        return a list of winners (a list that may only have one element most of
        the times), where each element of that list is a two-tuple:
            (vote_count, candidate)
        """
