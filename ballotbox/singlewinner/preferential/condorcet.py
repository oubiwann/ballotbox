import itertools

from zope.interface import implements

from ballotbox.criteria import (
    ICondorcetCriterion, IMajorityCriterion, ISmithCriterion)
from ballotbox.iballot import IVotingMethod
from ballotbox.singlewinner.preferential import base


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
