import itertools

from zope.interface import implements

from ballotbox.criteria import (
    ICondorcetCriterion, ICondorcetLoserCriterion,
    IIndependenceOfClonesCriterion, IMajorityCriterion, IMonotonicityCriterion,
    ISmithCriterion)
from ballotbox.iballot import IVotingMethod
from ballotbox.singlewinner.preferential import base, borda


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


class KemenyYoungVoting(base.PairWiseBase):
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


class NansonVoting(borda.StandardBordaVoting):
    """
    The Nanson method is based on the original work of the mathematician Edward
    J. Nanson.

    Nanson's method eliminates those choices from a Borda count tally that are
    at or below the average Borda count score, then the ballots are retallied
    as if the remaining candidates were exclusively on the ballot. This process
    is repeated if necessary until a single winner remains.

    The Nanson method and the Baldwin method satisfy the Condorcet criterion:
    since Borda always gives any existing Condorcet winner more than the
    average Borda points, the Condorcet winner will never be eliminated. They
    do not satisfy the independence of irrelevant alternatives criterion, the
    monotonicity criterion, the participation criterion, the consistency
    criterion and the independence of clones criterion, while they do satisfy
    the majority criterion, the mutual majority criterion, the Condorcet loser
    criterion, and the Smith criterion. The Nanson method satisfies reversal
    symmetry, while the Baldwin method violates reversal symmetry.

    Nanson's method was used in city elections in the U.S. town of Marquette,
    Michigan in the 1920s. It was formally used by the Anglican Diocese of
    Melbourne and in the election of members of the University Council of the
    University of Adelaide. It was used by the University of Melbourne until
    1983.
    """
    implements(
        IVotingMethod, IMajorityCriterion, ISmithCriterion)

    def _get_new_ballotbox(self, ballotbox):
        klass = ballotbox.__class__
        return klass(method=self.__class__)

    def _get_dropped_candidates(self, ballotbox):
        """
        Drop the candidates whose scores are lower than the average Borda score
        of all candidates in the ballotbox.
        """
        counts = self.get_counts(ballotbox)
        points = [count for count, candidate in counts]
        average = sum(points)/float(len(counts))
        return [candidate for count, candidate in counts if count < average]

    def iterate(self, ballotbox):
        new_ballotbox = self._get_new_ballotbox(ballotbox)
        dropped = self._get_dropped_candidates(ballotbox)
        for preferences, votes in ballotbox.items():
            new_preferences = {}
            for candidate, rank in preferences.items():
                if candidate not in dropped:
                    new_preferences[candidate] = rank
            new_ballotbox.add_votes(new_preferences, votes)
        return new_ballotbox

    def get_winner(self, ballotbox):
        self.candidate_count = self.get_candidate_count(ballotbox)
        while len(ballotbox.keys()[0].keys()) > 1:
            ballotbox = self.iterate(ballotbox)
        return self.get_counts(ballotbox)


class BaldwinVoting(NansonVoting):
    """
    This variant was devised by Joseph M. Baldwin and works like this:
        Candidates are voted for on ranked ballots as in the Borda count. Then,
        the points are tallied in a series of rounds. In each round, the
        candidate with the fewest points is eliminated, and the points are
        re-tallied as if that candidate were not on the ballot.

    The Baldwin method satisfy the Condorcet criterion: since Borda always
    gives any existing Condorcet winner more than the average Borda points, the
    Condorcet winner will never be eliminated. It does not satisfy the
    independence of irrelevant alternatives criterion, the monotonicity
    criterion, the participation criterion, the consistency criterion and the
    independence of clones criterion, while it does satisfy the majority
    criterion, the mutual majority criterion, the Condorcet loser criterion,
    and the Smith criterion. Also, the Baldwin method violates reversal
    symmetry.
    """
    implements(
        IVotingMethod, ICondorcetCriterion, IMajorityCriterion)

    def _get_dropped_candidates(self, ballotbox):
        """
        Drop the candidates who has the lowest Borda score.
        """
        counts = self.get_counts(ballotbox)
        COUNT, CANDIDATE = (0, 1)
        return counts[-1][CANDIDATE]


class RankedPairsVoting(object):
    """
    Ranked pairs (RP) or the Tideman method is a voting system developed in
    1987 by Nicolaus Tideman that selects a single winner using votes that
    express preferences. RP can also be used to create a sorted list of
    winners.

    If there is a candidate who is preferred over the other candidates, when
    compared in turn with each of the others, RP guarantees that candidate will
    win. Because of this property, RP is (by definition) a Condorcet method.

    The RP procedure is as follows:

        1. Tally the vote count comparing each pair of candidates, and
           determine the winner of each pair (provided there is not a tie).
           
        2. Sort (rank) each pair, by the largest margin of victory first to
           smallest last.  "Lock in" each pair, starting with the one with the
           largest number of winning votes, and add one in turn to a graph as
           long as they do not create a cycle (which would create an
           ambiguity). The completed graph shows the winner.

        3. RP can also be used to create a sorted list of preferred candidates.
           To create a sorted list, repeatedly use RP to select a winner,
           remove that winner from the list of candidates, and repeat (to find
           the next runner up, and so forth).

    Tally:

        To tally the votes, consider each voter's preferences. For example, if
        a voter states "A > B > C" (A is better than B, and B is better than
        C), the tally should add one for A in A vs. B, one for A in A vs. C,
        and one for B in B vs. C. Voters may also express indifference (e.g., A
        = B), and unstated candidates are assumed to be equally worse than the
        stated candidates.

        Once tallied the majorities can be determined. If "Vxy" is the number
        of Votes that rank x over y, then "x" wins if Vxy > Vyx, and "y" wins
        if Vyx > Vxy.
   
    Sort:

        The pairs of winners, called the "majorities", are then sorted from the
        largest majority to the smallest majority. A majority for x over y
        precedes a majority for z over w if and only if one of the following
        conditions holds:

            1. Vxy > Vzw. In other words, the majority having more support for
               its alternative is ranked first.

            2. Vxy = Vzw and Vwz > Vyx. Where the majorities are equal, the
               majority with the smaller minority opposition is ranked first.
        
    Lock:

        The next step is to examine each pair in turn to determine which pairs
        to "lock in". This can be visualized by drawing an arrow from the
        pair's winner to the pair's loser in a directed graph. Using the sorted
        list above, lock in each pair in turn unless the pair will create a
        circularity in the graph (e.g., where A is more than B, B is more than
        C, but C is more than A).

    Winner:

        In the resulting graph, the source corresponds to the winner. A source
        is bound to exist because the graph is a directed acyclic graph by
        construction, and such graphs always have sources. In the absence of
        pairwise ties, the source is also unique (because whenever two nodes
        appear as sources, there would be no valid reason not to connect them,
        leaving only one of them as a source).

    Of the formal voting system criteria, the ranked pairs method passes the
    majority criterion, the monotonicity criterion, the Condorcet criterion,
    the Condorcet loser criterion, and the independence of clones criterion.
    Ranked pairs fails the consistency criterion and the participation
    criterion. While ranked pairs is not fully independent of irrelevant
    alternatives, it does satisfy local independence of irrelevant
    alternatives.
    """
    implements(
        IVotingMethod, IMajorityCriterion, IMonotonicityCriterion,
        ICondorcetCriterion, ICondorcetLoserCriterion,
        IIndependenceOfClonesCriterion)

    def get_winner(self, ballotbox):
        pass


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
    implements(IVotingMethod)

    def __init__(self):
        raise NotImplementedError()
