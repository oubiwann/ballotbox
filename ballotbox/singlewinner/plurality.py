"""
The plurality voting system is a single-winner voting system often used to
elect executive officers or to elect members of a legislative assembly which is
based on single-member constituencies. This voting method is also used in
multi-member constituencies in what is referred to as an exhaustive counting
system where one member is elected at a time and the process repeated until the
number of vacancies is filled.

The most common system, used in Canada, India, the United Kingdom, and some
United States elections, is simple plurality, first-past-the-post or
winner-takes-all. In this voting system the single winner is the person with
the most votes; there is no requirement that the winner gain an absolute
majority of votes.

In some countries such as France (as well as in some jurisdictions of the
United States, such as Louisiana and Georgia) a similar system is used, but
there are two rounds: the "two-ballot" or "runoff election" plurality system.
If any candidate in the first round gains a majority of votes, then there is no
second round; otherwise, the two highest-voted candidates of the first round
compete in a two-candidate second round or all candidates above a certain
threshold in the first round compete in a two-, three- or four-candidate second
round.

In political science, the use of the plurality voting system alongside
multiple, single-winner constituencies to elect a multi-member body is often
referred to as single-member district plurality or SMDP. Plurality voting is
also variously referred to as winner-takes-all or relative/simple majority
voting; however, these terms can also refer to elections for multiple winners
in a particular constituency using bloc voting.
"""
from zope.interface import implements

from ballotbox.iballot import IVotingMethod


class FirstPastPostVoting(object):
    """
    First-past-the-post (abbreviated FPTP or FPP) voting refers to an election
    won by the candidate(s) with the most votes. The winning candidate does not
    necessarily receive an absolute majority of all votes cast. The system is
    also known as the 'winner-take-all' system, in which the candidate with the
    most votes gets elected.

    First-past-the-post voting methods can be used for single and multiple
    member elections. In a single member election the candidate with the
    highest number, not necessarily a majority, of votes is elected. The
    two-round ('runoff') voting system uses a first-past-the-post voting method
    in each of the two rounds. The first round determines which two candidates
    will progress to the second, final round ballot.
    
    In a multiple member first-past-the-post ballot, the first number of
    candidates, in order of highest vote, corresponding to the number of
    positions to be filled are elected. If there are six vacancies then the
    first six candidates with the highest vote are elected. A multiple
    selection ballot where more than one candidate can be voted for is also a
    form of first-past-the-post voting in which voters are allowed to cast a
    vote for as many candidates as there are vacant positions; the candidate(s)
    with the highest number of votes is elected.
    """
    implements(IVotingMethod)

    def get_winner(self, ballotbox, position_count=1):
        """
        """
        results = sorted([(count, name) for name, count in ballotbox.items()],
                         reverse=True)
        return results[0:position_count]


class TwoRoundVoting(object):
    """
    Note that this is simply a place-holder; there is no reason to implement
    two-round voting, as:
        1) one simply combined two other implementations, and
        2) for the second round, a re-vote is held

    As such, from an implementation standpoint, there is simply no need.

    For informational purposes:

    The two-round system (also known as the second ballot, runoff voting or
    ballotage) is a voting system used to elect a single winner where the voter
    casts a single vote for their chosen candidate. However, if no candidate
    receives the required number of votes (usually the absolute majority or
    40-45% with a winning margin of 5-15%), then those candidates having less
    than a certain proportion of the votes, or all but the two candidates
    receiving the most votes, are eliminated, and a second round of voting
    occurs.  
    
    The two round system is used around the world for the election of
    legislative bodies and directly elected presidents. For example, it is used
    in French presidential, legislative, and cantonal elections, and also to
    elect the presidents of Afghanistan, Argentina, Austria, Brazil, Bulgaria,
    Chile, Colombia, Croatia, Cyprus, Dominican Republic, Finland, Ghana,
    Guatemala, Indonesia, Poland, Portugal, Romania, Serbia, Slovakia,
    Slovenia, Ukraine, Uruguay, Zimbabwe. Historically it was used in the
    German Empire of 1871-1918, and in New Zealand in the 1908 and 1911
    elections.
    
    In both rounds of an election conducted using runoff voting, the voter
    simply marks an "X" beside his/her favorite candidate. If no candidate has
    an absolute majority of votes (i.e. more than half) in the first round,
    then the two candidates with the most votes proceed to a second round, from
    which all others are excluded. In the second round, because there are only
    two candidates, one candidate will achieve an absolute majority. In the
    second round each voter is entirely free to change the candidate he votes
    for, even if his preferred candidate has not yet been eliminated but he has
    merely changed his mind.

    Some variants of the two round system use a different rule for choosing
    candidates for the second round, and allow more than two candidates to
    proceed to the second round. Under these systems it is sufficient for a
    candidate to receive a plurality of votes (i.e. more votes than anyone
    else) to be elected in the second round. In elections for the French
    National Assembly any candidate with fewer than 12.5% of the total vote is
    eliminated in the first round, and all remaining candidates are permitted
    to stand in the second round, in which a plurality is sufficient to be
    elected. Under some variants of runoff voting there is no formal rule for
    eliminating candidates, but, rather, candidates who receive few votes in
    the first round are expected to withdraw voluntarily. The President of
    Weimar Germany was popularly elected in 1925 and 1932 by a two-round system
    that in the second round allowed any candidate to run and did not require
    an absolute majority. In both elections the Communist candidate Ernst
    Thalmann did not withdraw and ran in the second round; in 1925 this
    probably ensured the election of Paul von Hindenburg (with only 48.3% of
    the vote) rather that Wilhelm Marx, the candidate of the centre parties.
    """
    implements(IVotingMethod)

    def get_winner(self, ballotbox):
        raise NotImplementedError()


class ExhaustiveBallotVoting(object):
    """
    Similar to two-round voting, there is no reason to implement this. It
    requires direct interaction at each stage (each stage require a new
    BallotBox instance, with new votes).

    For more information:

    The exhaustive ballot is a voting system used to elect a single winner.
    Under the exhaustive ballot the elector simply casts a single vote for his
    or her favorite candidate. However if no candidate is supported by an
    overall majority of votes then the candidate with the fewest votes is
    eliminated and a further round of voting occurs. This process is repeated
    for as many rounds as necessary until one candidate has a majority.
    
    The exhaustive ballot is similar to the two-round system but with key
    differences. Under the two round system if no candidate wins a majority on
    the first round, only the top two recipients of votes advance to the second
    (and final) round of voting, and a majority winner is determined in the
    second round. By contrast, on the exhaustive ballot only one candidate is
    eliminated per round; thus, several rounds of voting may by required until
    a candidate reaches a majority.

    Because voters may have to cast votes several times, the exhaustive ballot
    is not used in large-scale public elections. Instead it is usually used in
    elections involving, at most, a few hundred voters, such as the election of
    a prime minister or the presiding officer of an assembly. The exhaustive
    ballot is currently used, in different forms, to elect the members of the
    Swiss Federal Council, the First Minister of Scotland, the President of the
    European Parliament, and the speakers of the Canadian House of Commons, the
    British House of Commons and the Scottish Parliament. It is also used to
    elect the various party nominees for President of the United States, the
    host city of the Olympic Games, the host of the FIFA World Cup, and in the
    Papal Conclave.
    """
    implements(IVotingMethod)

    def get_winner(self, ballotbox):
        raise NotImplementedError()
