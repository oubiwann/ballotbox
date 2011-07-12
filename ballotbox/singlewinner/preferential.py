from zope.interface import implements

from ballotbox.criteria import ICondorcetCriterion
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
    implements = (IVotingMethod, ICondorcetCriterion)

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


class KemenyYoungVoting(object):
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
    implements = (IVotingMethod, ICondorcetCriterion)

    def get_winner(self, ignored, ballotboxes, position_count=1):
        data = {}
        for box in ballotboxes:

    return results[0:position_count]


class MajorityCriterion(object):
    """
    The majority criterion is a single-winner voting system criterion, used to
    compare such systems. The criterion states that "if one candidate is
    preferred by a majority (more than 50%) of voters, then that candidate must
    win".

    Some methods that comply with this criterion include any Condorcet method,
    instant-runoff voting, and Bucklin voting.

    Some methods which give weight to preference strength fail the majority
    criterion, while others pass it. Thus the Borda count and range voting fail
    the majority criterion, while the Majority judgment passes it. The
    application of the majority criterion to methods which cannot provide a
    full ranking, such as approval voting, is disputed.

    These methods that fail the majority criterion may offer a strategic
    incentive to voters to bullet vote, i.e., vote for one candidate only, not
    providing any information about their possible support for other
    candidates, since, with such methods, these additional votes may aid their
    less-preferred.
    """


class CondorcetCriterion(MajorityCriterion):
    """
    The Condorcet candidate or Condorcet winner of an election is the candidate
    who, when compared with every other candidate, is preferred by more voters.
    Informally, the Condorcet winner is the person who would win a
    two-candidate election against the other candidate. A Condorcet winner will
    not always exist in a given set of votes, which is known as Condorcet's
    voting paradox. When voters identify candidates on a left-to-right axis and
    always prefer candidates closer to themselves, a Condorcet winner always
    exists.

    A voting system satisfies the Condorcet criterion if it chooses the
    Condorcet winner when one exists. Any method conforming to the Condorcet
    criterion is known as a Condorcet method.

    It is named after the 18th century mathematician and philosopher Marie Jean

    Antoine Nicolas Caritat, the Marquis de Condorcet.
    """


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



