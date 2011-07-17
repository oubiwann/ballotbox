import json

from zope.interface import implements

from ballotbox.iballot import IBallotBox


class BallotBox(dict):
    """
    """
    implements(IBallotBox)

    def __init__(self, method=None, data={}, *args, **kwargs):
        super(BallotBox, self).__init__(data)
        # instantiate the voting method class
        if method:
            #import pdb;pdb.set_trace()
            method = method(*args, **kwargs)
        self.method = method

    # XXX looks like we should do a decorator for all of these calls
    def __getitem__(self, key):
        """
        x.__getitem__(y) <==> x[y]
        """
        key = self._encode(key)
        return super(BallotBox, self).__getitem__(key)

    def __setitem__(self, key, value):
        """
        x.__setitem__(i, y) <==> x[i]=y
        """
        key = self._encode(key)
        super(BallotBox, self).__setitem__(key, value)

    def has_key(self, key):
        """
        D.has_key(k) -> True if D has a key k, else False.
        """
        key = self._encode(key)
        super(BallotBox, self).has_key(key)

    def items(self):
        """
        D.items() -> list of D's (key, value) pairs, as 2-tuples.
        """
        data = super(BallotBox, self).items()
        return [(self._decode(key), value) for key, value in data]

    def keys(self):
        """
        D.keys() -> list of D's keys.
        """
        data = super(BallotBox, self).keys()
        return [self._decode(key) for key in data]

    def iteritems(self):
        """
        D.iteritems() -> an iterator over the (key, value) items of D.
        """
        for key, value in super(BallotBox, self).iteritems():
            key = self._decode(key)
            yield key, value

    def iterkeys(self):
        """
        D.iterkeys() -> an iterator over the keys of D.
        """
        for key in super(BallotBox, self).iterkeys():
            key = self._decode(key)
            yield json.loads(key)

    def update(self, vote):
        """
        D.update(E, **F) -> None.  Update D from dict/iterable E and F.

         * If E has a .keys() method, does:     for k in E: D[k] = E[k]

         * If E lacks .keys() method, does:     for (k, v) in E: D[k] = v

        In either case, this is followed by: for k in F: D[k] = F[k]
        """
        data = [(self._encode(key), value) for key, value in vote.items()]
        super(BallotBox, self).update(dict(data))

    def _is_string(self, data):
        if isinstance(data, basestring):
            return True
        return False

    def _encode(self, data):
        if isinstance(data, list) or isinstance(data, dict):
            data = json.dumps(data)
        return data

    def _decode(self, data):
        try:
            return json.loads(data)
        except ValueError:
            return data

    def add_vote(self, vote):
        """
        The parameter 'vote' can be either a single string representing a
        candidate, or a dictionary representing a set of preferences cast by a
        single voter.
        """
        vote = self._encode(vote)
        self.setdefault(vote, 0)
        self[vote] += 1

    def add_votes(self, vote, count):
        """
        For a unique vote, add the number of times it was voted for.
        """
        vote = self._encode(vote)
        self.setdefault(vote, 0)
        self[vote] += count

    def batch_votes(self, votes):
        """
        This method differs from the add_votes method in that there is more
        than one vote being cast, each with potentially many vote counts.

        The parameter 'votes' should be a list of tuples:
            [(vote1, count1), (vote2, count2), ... (voten, countn)]
        """
        for vote, count in votes:
            self.add_votes(vote, count)

    def get_total_votes(self):
        """
        Count all votes cast for all candidates.
        """
        return sum(self.values())

    def get_winner(self, *args, **kwargs):
        """
        Determine the winner, if one exists.

        This is a wrapper for the method of the same name on the IVotingMethod
        implementation class.
        """
        return self.method.get_winner(self, *args, **kwargs)
