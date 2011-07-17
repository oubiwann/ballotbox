from zope.interface import implements

from ballotbox.criteria import (
    ICondorcetCriterion, IMajorityCriterion, IPluralityCriterion)
from ballotbox.iballot import IVotingMethod
from ballotbox.singlewinner.preferential import base


class MinimaxWinningVoting(base.PairWiseBase):
    """
    The number of voters ranking x above y, but only when this score exceeds
    the number of voters ranking y above x. If not, then the score for x
    against y is zero. This is sometimes called winning votes.

    See the MinimaxVoting factory function's docstring for more information.

    XXX This implementation may not be correct; I'm not sure the wikipedia
    article gave enough information to accurately define it.
    """
    implements(
        IVotingMethod, ICondorcetCriterion, IMajorityCriterion,
        IPluralityCriterion)

    def get_winner(self, ballotbox, candidate1, candidate2):
        self.lookup = self.build_lookup(ballotbox)
        [(votes_for, comparison), 
         (votes_against, anti_comparison)] = self._compare(
            candidate1, candidate2)
        rank = votes_for - votes_against
        if rank < 0:
            votes_for = 0
        return [(votes_for, comparison)]


class MinimaxMarginsVoting(base.PairWiseBase):
    """
    The number of voters ranking x above y minus the number of voters ranking y
    above x. This is called using margins.

    See the MinimaxVoting factory function's docstring for more information.

    XXX This implementation may not be correct; I'm not sure the wikipedia
    article gave enough information to accurately define it.
    """
    implements(
        IVotingMethod, ICondorcetCriterion, IMajorityCriterion)

    def get_winner(self, ballotbox, candidate1, candidate2):
        self.lookup = self.build_lookup(ballotbox)
        [(votes_for, comparison), 
         (votes_against, anti_comparison)] = self._compare(
            candidate1, candidate2)
        rank = votes_for - votes_against
        return [(rank, comparison)]


class MinimaxPairwiseOppositionVoting(base.PairWiseBase):
    """
    The number of voters ranking x above y, regardless of whether more voters
    rank x above y or vice versa. This interpretation is sometimes called
    pairwise opposition.

    See the MinimaxVoting factory function's docstring for more information.

    XXX This implementation may not be correct; I'm not sure the wikipedia
    article gave enough information to accurately define it.
    """
    implements(IVotingMethod)

    def get_winner(self, ballotbox, candidate1, candidate2):
        self.lookup = self.build_lookup(ballotbox)
        [(votes_for, comparison), 
         (votes_against, anti_comparison)] = self._compare(
            candidate1, candidate2)
        return [(votes_for, comparison)]


def MinimaxVoting(mode="winning votes"):
    """
    The 'mode' parameter can be one of the following:
        * "winning votes"
        * "margins"
        * "pairwise opposition"

    Minimax is often considered to be the simplest of the Condorcet
    methods. It is also known as the Simpson-Kramer method, and the successive
    reversal method.

    Minimax selects the candidate for whom the greatest pairwise score for
    another candidate against him is the least such score among all candidates.

    Formally, let score(X,Y) denote the pairwise score for X against Y. Then
    the candidate, W selected by minimax (aka the winner) is given by:

        W = argminX(maxYscore(Y,X))

    When it is permitted to rank candidates equally, or to not rank all the
    candidates, three interpretations of the rule are possible. When voters
    must rank all the candidates, all three rules are equivalent.

    The score for candidate x against y can be defined as:

        1. The number of voters ranking x above y, but only when this score
           exceeds the number of voters ranking y above x. If not, then the
           score for x against y is zero. This is sometimes called winning
           votes.

        2. The number of voters ranking x above y minus the number of voters
           ranking y above x. This is called using margins.

        3. The number of voters ranking x above y, regardless of whether more
           voters rank x above y or vice versa. This interpretation is
           sometimes called pairwise opposition.

    When one of the first two interpretations is used, the method can be
    restated as: "Disregard the weakest pairwise defeat until one candidate is
    unbeaten." An "unbeaten" candidate possesses a maximum score against him
    which is zero or negative.

    Minimax using winning votes or margins satisfies Condorcet and the majority
    criterion, but not the Smith criterion, mutual majority criterion,
    independence of clones criterion, or Condorcet loser criterion. When
    winning votes is used, Minimax also satisfies the Plurality criterion.

    When the pairwise opposition interpretation is used, minimax also does not
    satisfy the Condorcet criterion. However, when equal-ranking is permitted,
    there is never an incentive to put one's first-choice candidate below
    another one on one's ranking. It also satisfies the Later-no-harm
    criterion, which means that by listing additional, lower preferences in
    one's ranking, one cannot cause a preferred candidate to lose.
    """
    # note that a factory is used here due to the fact that different minimax
    # classes satisfy different criteria
    if mode == "winning votes":
        return MinimaxWinningVoting()
    elif mode == "margins":
        return MinimaxMarginsVoting()
    elif mode == "pairwise opposition":
        return MinimaxPairwiseOppositionVoting()
    else:
        raise ValueError("Unknown mode '%'" % mode)
