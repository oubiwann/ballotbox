import itertools

from zope.interface import implements

from ballotbox.criteria import (
    ICondorcetCriterion, IMajorityCriterion, ISmithCriterion)
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
