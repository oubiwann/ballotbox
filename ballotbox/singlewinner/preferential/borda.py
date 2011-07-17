

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
