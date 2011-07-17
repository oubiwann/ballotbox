from zope.interface import Attribute, Interface


class IBallotBox(Interface):
    """
    """
    method = Attribute("The voting methodology used (a *Voting instance)")

    def add_vote(self, vote):
        """
        Add a single vote at a time.

        The parameter 'vote' can be either a single string representing a
        candidate, or a dictionary representing a set of preferences cast by a
        single voter.
        """

    def add_votes(self, vote, count):
        """
        For a unique vote, add the number of times it was voted for.
        """

    def batch_votes(self, votes):
        """
        This method differs from the add_votes method in that there is more
        than one vote being cast, each with potentially many vote counts.

        The parameter 'votes' should be a list of tuples:
            [(vote1, count1), (vote2, count2), ... (voten, countn)]
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
