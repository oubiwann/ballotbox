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

    # XXX looks like we should do a decorator for all of these calls
    def __getitem__(self, key):
        key = self._encode(key)
        return super(BallotBox, self).__getitem__(key)

    def __setitem__(self, key, value):
        key = self._encode(key)
        super(BallotBox, self).__setitem__(key, value)

    def has_key(self, key):
        key = self._encode(key)
        super(BallotBox, self).has_key(key)

    def items(self):
        data = super(BallotBox, self).items()
        return [(self._decode(key), value) for key, value in data]

    def keys(self):
        data = super(BallotBox, self).keys()
        return [self._decode(key) for key in data]

    def iteritems(self):
        for key, value in super(BallotBox, self).iteritems():
            key = self._decode(key)
            yield key, value

    def iterkeys(self):
        for key in super(BallotBox, self).iterkeys():
            key = self._decode(key)
            yield json.loads(key)

    def _update(self, vote):
        data = [(self._encode(key), value) for key, value in vote.items()]
        super(BallotBox, self).update(dict(data))

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
        return sum(self.values())

    def get_winner(self, *args, **kwargs):
        return self.method.get_winner(self, *args, **kwargs)
