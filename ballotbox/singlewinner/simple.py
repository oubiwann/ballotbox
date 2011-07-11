from zope.interface import implements
from decimal import Decimal

from ballotbox.iballot import IVotingMethod


class MajorityRuleVoting(object):
    """
    Majority rule is a decision rule that selects alternatives which have a
    majority, that is, more than half the votes

    Though plurality (first-past-the post) is often mistaken for majority rule,
    they are not the same. Plurality makes the options with the most votes the
    winner, regardless of whether the fifty percent threshold is passed.  This
    is equivalent to majority rule when there are only two alternatives.
    However, when there are more than two alternatives, it is possible for
    plurality to choose an alternative that has fewer than fifty percent of the
    votes cast in its favor.
    """
    implements(IVotingMethod)

    def get_winner(self, ballotbox):
        total_votes = ballotbox.get_total_votes()
        winner = []
        for name, votes in ballotbox.items():
            fraction = Decimal(votes) / Decimal(total_votes)
            if fraction > Decimal(".5"):
                winner = [(votes, name)]
        return winner
