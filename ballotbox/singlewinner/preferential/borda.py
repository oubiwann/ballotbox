

class StandardBordaVoting(object):
    """
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
    def __init__(self):
        self.candidate_count = 0

    def get_candidates(self, ballotbox):
        preferences = ballotbox.keys()[0]
        return preferences.keys()

    def get_candidate_count(self, ballotbox):
        return len(self.get_candidates(ballotbox))

    def get_points(self, rank):
        return self.candidate_count - rank

    def get_counts(self, ballotbox):
        totals = {}
        for preferences, votes in ballotbox.items():
            for candidate, rank in preferences.items():
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
    In the Parliament of Nauru, a distinctive formula is used based on
    increasingly small fractions of points. Under the system a candidate
    receives 1 point for a first preference, 1/2, a point for a second
    preference, 1/3 for third preference, and so on. This method is far more
    favourable to candidates with many first preferences than the conventional
    Borda count; it also substantially reduces the impact of electors
    indicating late preferences at random because they have to complete the
    full ballot.

    See the StandardBordaVoting factory function's docstring for more
    information.
    """
    def get_points(self, rank):
        return 1/float(rank)


class TruncatedBordaVoting(StandardBordaVoting):
    """
    A common way in which versions of the Borda count differ is the method for
    dealing with truncated ballots, that is, ballots on which a voter has not
    expressed a full list of preferences. There are several methods:

    The simplest method is to allow voters to rank as many or as few candidates
    as they wish, but simply give every unranked candidate the minimum number
    of points. For example, if there are 10 candidates, and a voter votes for
    candidate A first and candidate B second, leaving everyone else unranked,
    candidate A receives 9 points, candidate B receives 8, and all other
    candidates receive 0 points. However, this method allows strategic voting
    in the form of bullet voting: voting for only one candidate and leaving
    every other candidate unranked. This variant makes a bullet vote more
    effective than a fully-ranked ballot.

    See the StandardBordaVoting factory function's docstring for more
    information.
    """
    def get_points(self, rank):
        if rank > 0:
            points = self.candidate_count - rank
        else:
            points = 0
        return points


class ModifedBordaVoting(StandardBordaVoting):
    """
    In a modified Borda count (MBC), the number of points given for a voter's
    first and subsequent preferences is determined by the total number of
    candidates they have actually ranked, rather than the total number
    standing. This is to say, typically, on a ballot of n options/candidates,
    if a voter casts preferences for only m options (where m is smaller than
    n), a first preference gets m points, a second preference m-1 points, and
    so on. This means, in other words, that if there are ten candidates but a
    voter ranks only five, then their first preference will receive only five
    points; their second preference will receive 4 points, their next 3, and so
    on. This method effectively penalises voters who do not rank a full ballot,
    by diminishing the number of points their vote distributes among
    candidates.

    Thus he who votes for only one option/candidate exercises only 1 point;
    while she who casts two preferences will exercise 3 (2+1) points.

    In more general terms, an 'x'th preference, if cast, gets one more point
    than an 'x+1'th preference (whether cast or not). The MBC involves no
    special weighting: the difference is always just one point.

    It is also possible, if specifically stipulated by the body using the MBC
    as its voting method, that candidates voted for by someone who does not
    cast preferences for all candidates get even less points than described
    above. For example, the first preference listed may receive m-1 points
    instead of m points, the second preference will then receive m-2 points,
    and so on.

    The modified Borda count differs from a Borda count only in the preferences
    of those who submit partial ballots. In a BC on five options, he who votes
    for all five options gives his first preference 5 points, his second
    preference 4 points, and so on and she who votes for only one option still
    gives her first preference 5 points. In effect, therefore, a modified Borda
    count encourages the voter to submit only a first preference, in which case
    it degenerates into a plurality vote.

    In a five-option MBC, by contrast, she who votes for only one option thus
    gives her favourite just 1 point; he who votes for two options gives his
    first preference 2 points (and his second preference 1 point). To ensure
    your favourite gets the maximum 5 points, therefore, you should cast all
    five preferences, then your favourite gets 5 points, your second preference
    gets 4 points, and so on, just like in a Borda count. The MBC thus
    encourages voters to submit a fully marked ballot.

    See the StandardBordaVoting factory function's docstring for more
    information.
    """
    def get_points(self, preferences, rank):
        candidates = preferences.keys()
        count = len(candidates)
        return count - rank

    def get_counts(self, ballotbox):
        totals = {}
        for preferences, votes in ballotbox.items():
            for candidate, rank in preferences.items():
                totals.setdefault(candidate, 0)
                totals[candidate] += self.get_points(preferences, rank) * votes
        return sorted(
            [(count, candidate) for candidate, count in totals.items()],
            reverse=True)


def BordaVoting(mode="standard", *args, **kwargs):
    """
    The 'mode' parameter can be one of the following:
        * "standard"
        * "fractional"
        * "truncated"
        * "modified"

    This factory function returns a borda voting instance.
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
