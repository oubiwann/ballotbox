import itertools

from zope.interface import implements

from ballotbox.criteria import (
    ICondorcetCriterion, IMajorityCriterion, IPluralityCriterion,
    ISmithCriterion)
from ballotbox.iballot import IVotingMethod


class CopelandVoting(object):
    """
    Copeland's method or Copeland's pairwise aggregation method is a Condorcet
    method in which candidates are ordered by the number of pairwise victories,
    minus the number of pairwise defeats.

    Proponents argue that this method is easily understood by the general
    populace, which is generally familiar with the sporting equivalent. In many
    round-robin tournaments, the winner is the competitor with the most
    victories.

    Copeland requires a Smith set containing at least five candidates to give a
    clear winner unless two or more candidates tie in pairwise comparisons.
    """
    implements(IVotingMethod, ICondorcetCriterion)

    def get_winner(self, ignored, ballotboxes):
        data = {}
        for box in ballotboxes:
            candidates = set(box.keys())
            for candidate in candidates:
                data.setdefault(candidate, {"wins": 0, "losses": 0})
            [(votes, winner)] = box.get_winner()
            loser = (candidates - set(winner)).pop()
            data[winner]["wins"] += 1
            data[loser]["losses"] += 1
        results = sorted([
            (stats['wins'] - stats['losses'], candidate)
            for candidate, stats in data.items()], reverse=True)
        return [results[0]]


class PairWiseBase(object):
    """
    This is a base class to hold common code for implementations that utilize
    pair-wise comparisons.
    """
    def __init__(self):
        self.preference_options = []
        self.lookup = {}

    def build_lookup(self, ballotbox):
        pairs = {}
        for preferences, votes in ballotbox.items():
            preference_list = preferences.items()
            # let's get a list of options for later use
            if not self.preference_options:
                self.preference_options = [
                    option for option, rank in preference_list]
            for index, preference1 in enumerate(preference_list[:-1]):
                for preference2 in preference_list[index + 1:]:
                    option1, rank1 = preference1
                    option2, rank2 = preference2
                    # remember, first choice is "1" and that's a lower number
                    # than "2", so the lower the amount, the greater the
                    # preference
                    if rank1 < rank2:
                        lookup = "%s > %s" % (option1, option2)
                    elif rank2 < rank1:
                        lookup = "%s > %s" % (option2, option1)
                    else:
                        lookup = "%s = %s" % (option1, option2)
                    pairs.setdefault(lookup, 0)
                    pairs[lookup] += votes
        return pairs

    def _compare(self, candidate1, candidate2):
        comparison = "%s > %s" % (candidate1, candidate2)
        anti_comparison = "%s > %s" % (candidate2, candidate1)
        votes_for = self.lookup[comparison]
        votes_against = self.lookup[anti_comparison]
        return [(votes_for, comparison), (votes_against, anti_comparison)]


class KemenyYoungVoting(PairWiseBase):
    """
    The Kemeny-Young method is a voting system that uses preferential ballots
    and pairwise comparison counts to identify the most popular choices in an
    election. It is a Condorcet method because if there is a Condorcet winner,
    it will always be ranked as the most popular choice.

    This method assigns a score for each possible sequence, where each sequence
    considers which choice might be most popular, which choice might be
    second-most popular, which choice might be third-most popular, and so on
    down to which choice might be least-popular. The sequence that has the
    highest score is the winning sequence, and the first choice in the winning
    sequence is the most popular choice. (As explained below, ties can occur at
    any ranking level.)

    The Kemeny-Young method is also known as the Kemeny rule, VoteFair
    popularity ranking, the maximum likelihood method, and the median relation.

    The Kemeny-Young method uses preferential ballots on which voters rank
    choices according to their order of preference. A voter is allowed to rank
    more than one choice at the same preference level. Unranked choices are
    usually interpreted as least-preferred.

    Another way to view the ordering is that it is the one which minimizes the
    sum of the Kendall tau distances (bubble sort distance) to the voters'
    lists.

    Kemeny-Young calculations are usually done in two steps. The first step is
    to create a matrix or table that counts pairwise voter preferences. The
    second step is to test all possible rankings, calculate a score for each
    such ranking, and compare the scores. Each ranking score equals the sum of
    the pairwise counts that apply to that ranking.

    The ranking that has the largest score is identified as the overall
    ranking. (If more than one ranking has the same largest score, all these
    possible rankings are tied, and typically the overall ranking involves one
    or more ties.)
    """
    implements(IVotingMethod, ICondorcetCriterion)

    def get_ranks(self):
        ranks = []
        for possibility in itertools.permutations(self.preference_options):
            rank = 0
            for index, option1 in enumerate(possibility[:-1]):
                for option2 in possibility[index + 1:]:
                    key = "%s > %s" % (option1, option2)
                    rank += self.lookup[key]
            ranks.append((rank, possibility))
        return sorted(ranks, reverse=True)

    def get_winner(self, ballotbox, position_count=1):
        self.preference_options = []
        self.lookup = self.build_lookup(ballotbox)
        results = self.get_ranks()
        return results[0:position_count]


class MinimaxWinningVoting(PairWiseBase):
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


class MinimaxMarginsVoting(PairWiseBase):
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


class MinimaxPairwiseOppositionVoting(PairWiseBase):
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


class StandardBordaVoting(object):
    """
    """
    def __init__(self):
        self.candidate_count = 0

    def get_candidates(self, ballotbox):
        preference = ballotbox.keys()[0]
        return preference.keys()

    def get_candidate_count(self, ballotbox):
        return len(self.get_candidates(ballotbox))

    def get_points(self, rank):
        return self.candidate_count - rank
        
    def get_counts(self, ballotbox):
        totals = {}
        for preference, votes in ballotbox.items():
            for candidate, rank in preference.items():
                points = self.get_points(rank)
                totals.setdefault(candidate, 0)
                totals[candidate] += self.get_points(rank) * votes
        return sorted(
            [(count, candidate) for candidate, count in totals.items()],
            reverse=True)

    def get_winner(self, ballotbox):
        self.candidate_count = self.get_candidate_count(ballotbox)
        results = self.get_counts(ballotbox)
        return [results[0]]


class FractionalBordaVoting(StandardBordaVoting):
    """
    """
    def get_points(self, rank):
        return 1/float(rank)


class TruncatedBordaVoting(object):
    """
    """


class ModifedBordaVoting(object):
    """
    """


def BordaVoting(mode="standard", *args, **kwargs):
    """
    The 'mode' parameter can be one of the following:
        * "standard"
        * "fractional"
        * "truncated"
        * "modified"

    The Borda count is a single-winner election method in which voters rank
    candidates in order of preference. The Borda count determines the winner of
    an election by giving each candidate a certain number of points
    corresponding to the position in which he or she is ranked by each voter.
    Once all votes have been counted the candidate with the most points is the
    winner. Because it sometimes elects broadly acceptable candidates, rather
    than those preferred by the majority, the Borda count is often described as
    a consensus-based electoral system, rather than a majoritarian one.

    The Borda count was developed independently several times, but is named for
    the 18th-century French mathematician and political scientist Jean-Charles
    de Borda, who devised the system in 1770. It is currently used for the
    election of two ethnic minority members of the National Assembly of
    Slovenia, and, in modified forms, to select presidential election
    candidates in Kiribati and to elect members of the Parliament of Nauru. It
    is also used throughout the world by various private organisations and
    competitions.

    Under the Borda count the voter ranks the list of candidates in order of
    preference. So, for example, the voter gives a '1' to their first
    preference, a '2' to their second preference, and so on. In this respect, a
    Borda count election is the same as elections under other preferential
    voting systems, such as instant-runoff voting, the Single Transferable Vote
    or Condorcet's method.

    The number of points given to candidates for each ranking is determined by
    the number of candidates standing in the election. Thus, under the simplest
    form of the Borda count, if there are five candidates in an election then a
    candidate will receive five points each time they are ranked first, four
    for being ranked second, and so on, with a candidate receiving 1 point for
    being ranked last (or left unranked). In other words, where there are n
    candidates a candidate will receive n points for a first preference, n-1
    points for a second preference, n-2 for a third, and so on.
    """
    # note that a factory is used here due to the fact that different borda
    # classes satisfy suffer from very different vulnerabilities
    if mode == "standard":
        return StandardBordaVoting(*args, **kwargs)
    elif mode == "fractional":
        return FractionalBordaVoting(*args, **kwargs)
    elif mode == "truncated":
        return TruncatedBordaVoting(*args, **kwargs)
    elif mode == "modified":
        return ModifedBordaVoting(*args, **kwargs)
    else:
        raise ValueError("Unknown mode '%'" % mode)


class NansonVoting(object):
    """
    """
    implements(
        IVotingMethod, IMajorityCriterion, ISmithCriterion)


class BaldwinVoting(object):
    """
    """
    implements(
        IVotingMethod, ICondorcetCriterion, IMajorityCriterion)


class BucklinVoting(object):
    """
    Bucklin voting is a class of voting systems that can be used for
    single-member and multi-member districts. It is named after its original
    promoter, James W. Bucklin of Grand Junction, Colorado, and is also known
    as the Grand Junction system. As in Majority Judgment, the Bucklin winner
    will be one of the candidates with the highest median ranking or rating.

    Voters are allowed rank preference ballots (first, second, third, etc.).

    First choice votes are first counted. If one candidate has a majority, that
    candidate wins. Otherwise the second choices are added to the first
    choices. Again, if a candidate with a majority vote is found, the winner is
    the candidate with the most votes accumulated. Lower rankings are added as
    needed.

    A majority is determined based on the number of valid ballots. Since, after
    the first round, there may be more votes cast than voters, it is possible
    for more than one candidate to have majority support.
    """


class DodgsonVoting(object):
    """
    Dodgson's Method is a voting system proposed by Charles Dodgson.

    In Dodgson's method, each voter submits an ordered list of all candidates
    according to their own preference (from best to worst). The winner is
    defined to be the candidate for whom we need to perform the minimum number
    of pairwise swaps (added over all candidates) before they become a
    Condorcet winner. In particular, if there is already a Condorcet winner,
    they win the election.

    In short, we must find the voting profile with minimum Kendall tau distance
    from the input, such that it has a Condorcet winner; they are declared the
    victor. Computing the winner is an NP-hard problem.
    """



