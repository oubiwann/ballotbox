class RangeVoting(object):
    """
    Range voting (also called ratings summation, average voting, cardinal
    ratings, score voting, 0–99 voting, the score system, or the point system)
    is a voting system for one-seat elections under which voters score each
    candidate, the scores are added up, and the candidate with the highest
    score wins. 
    
    A form of range voting was apparently used in some elections in Ancient
    Sparta by measuring how loudly the crowd shouted for different candidates;
    rough modern-day equivalents include the use of clapometers in some
    television shows and the judging processes of some athletic competitions.

    Range voting satisfies the monotonicity criterion, i.e. raising your vote's
    score for a candidate can never hurt their chances of winning. Also, in
    range voting, casting a sincere vote can never result in a worse election
    winner (from your point of view) than if you had simply abstained from
    voting. Range voting passes the favorite betrayal criterion,[6] meaning
    that it never gives voters an incentive to rate their favorite candidate
    lower than a candidate they like less.
    """
    def __init__(self, range_values):
        self.range_values = range_values


class ApprovalVoting(RangeVoting):
    """
    Approval voting is a single-winner voting system used for elections. Each
    voter may vote for (or 'approve' of) as many of the candidates as the voter
    wishes. The winner is the candidate receiving the most votes. Each voter
    may vote for any combination of candidates and may give each candidate at
    most one vote.

    The system was described in 1976 by Guy Ottewell and also by Robert J.
    Weber, who coined the term "approval voting." It was more fully published
    in 1978 by political scientist Steven Brams and mathematician Peter
    Fishburn.

    Approval voting can be considered a form of range voting, with the range
    restricted to two values, 0 and 1, or a form of Majority Judgment, with the
    grades restricted to "Good" and "Poor". Approval voting can also be
    compared to plurality voting, without the rule that discards ballots which
    vote for more than one candidate.

    Ballots which mark every candidate the same (whether yes or no) have no
    effect on the outcome of the election. Each ballot can therefore be viewed
    as a small "delta" which separates two groups of candidates, or a
    single-pair of ranks (e.g. if a ballot indicates that A & C are approved
    and B & D are not, the ballot can be considered to convey the ranking
    [A=C]>[B=D]).
    """
    range_values = [0, 1]


class MajorityJudgement(BucklinVoting):
    """
    Majority Judgment is a single-winner voting system proposed by Michel
    Balinski and Rida Laraki. Voters freely grade each candidate in one of
    several named ranks, for instance from "excellent" to "bad", and the
    candidate with the highest median grade is the winner. If more than one
    candidate has the same median grade, a tiebreaker is used which sees the
    "closest-to-median" grade. Majority Judgment can be considered as a form of
    Bucklin voting which allows equal ranks.

    Voters are allowed rated ballots, on which they may assign a grade or
    judgment to each candidate. Badinski and Laraki suggest six grading levels,
    from "Excellent" to "Reject". Multiple candidates may be given the same
    grade if the voter desires.

    The median grade for each candidate is found, for instance by sorting their
    list of grades and finding the middle one. If the middle falls between two
    different grades, the lower of the two is used.

    The candidate with the highest median grade wins. If several candidates
    share the highest median grade, all other candidates are eliminated. Then,
    one copy of that grade is removed from each remaining candidate's list of
    grades, and the new median is found, until there is an unambiguous winner.
    For instance, if candidate X's sorted ratings were {"Good", "Good", "Fair",
    "Poor"}, while candidate Y had {"Excellent", "Fair", "Fair", "Fair"}, the
    rounded medians would both be "Fair". After removing one "Fair" from each
    list, the new lists are, respectively, {"Good", "Good", "Poor"} and
    {"Excellent", "Fair", "Fair"}, so X would win with a recalculated median of
    "Good".
    """
