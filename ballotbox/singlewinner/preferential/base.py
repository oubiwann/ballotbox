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
