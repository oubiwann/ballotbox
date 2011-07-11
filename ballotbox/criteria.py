from zope.interface import Interface


class ICriterion(Interfac):
    """
    The base interface for all criteria.
    """


class IMajorityCriterion(ICriterion):
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


class IMajorityLoserCriterion(ICriterion):
    """
    The majority loser criterion is a criterion to evaluate single-winner
    voting systems. The criterion states that if a majority of voters prefers
    every other candidate over a given candidate, then that candidate must not
    win.

    Either of the Condorcet loser criterion or the mutual majority criterion
    imply the majority loser criterion. However, the Condorcet criterion does
    not imply the majority loser criterion. Neither does the majority criterion
    imply the majority loser criterion.

    Methods that comply with this criterion include Schulze, Ranked Pairs,
    Kemeny-Young, Nanson, Baldwin, Coombs, Borda, Bucklin, instant-runoff
    voting, contingent voting, and anti-plurality voting.

    Methods that do not comply with this criterion include plurality, MiniMax,
    Sri Lankan contingent voting, supplementary voting, approval voting, and
    range voting.
    """


class IMutualMajorityCriterion(MajorityCriterion, MajorityLoserCriterion):
    """
    The mutual majority criterion is a criterion used to compare voting
    systems. It is also known as the majority criterion for solid coalitions
    and the generalized majority criterion. The criterion states: If there is a
    subset S of the candidates such that more than half of the voters strictly
    prefer every member of S to every candidate outside of S, and this majority
    votes sincerely, then the winner must come from S. This is similar to but
    more strict than the majority criterion, where the requirement applies only
    to the case that S contains a single candidate.

    Methods that pass: The Schulze method, ranked pairs, instant-runoff voting,
    Nanson's method, Bucklin voting.

    Methods that fail: plurality, approval voting, range voting, the Borda
    count, minimax.
    """


class IMonotonicityCriterion(ICriterion):
    """
    The monotonicity criterion is a voting system criterion used to analyze
    both single and multiple winner voting systems. A voting system is
    monotonic if it satisfies one of the definitions of the monotonicity
    criterion, given below.

    Douglas R. Woodall, calling the criterion mono-raise, defines it as:
        A candidate x should not be harmed [i.e., change from being a winner to
        a loser] if x is raised on some ballots without changing the orders of
        the other candidates.

    Note that the references to orders and relative positions concern the
    rankings of candidates other than X, on the set of ballots where X has been
    raised. So, if changing a set of ballots voting "A > B > C" to "B > C > A"
    causes B to lose, this does not constitute failure of Monotonicity, because
    in addition to raising B, we changed the relative positions of A and C.
    This criterion may be intuitively justified by reasoning that in any fair
    voting system, no vote for a candidate, or increase in the candidate's
    ranking, should instead hurt the candidate. It is a property considered in
    Arrow's impossibility theorem. Some political scientists, however, doubt
    the value of monotonicity as an evaluative measure of voting systems. David
    Austen-Smith and Jeffrey Banks, for example, published an article in The
    American Political Science Review in which they argue that "monotonicity in
    electoral systems is a nonissue: depending on the behavioral model
    governing individual decision making, either everything is monotonic or
    nothing is monotonic."

    Although all voting systems are vulnerable to tactical voting, systems
    which fail the monotonicity criterion suffer an unusual form, where voters
    with enough information about other voter strategies could theoretically
    try to elect their candidate by counter-intuitively voting against that
    candidate. Tactical voting in this way presents an obvious risk if a
    voter's information about other ballots is wrong, however, and there is no
    evidence that voters actually pursue such counter-intuitive strategies in
    non-monotonic voting systems in real-world elections.

    Of the single-winner voting systems, plurality voting (first past the
    post), Borda count, Schulze method, and Ranked Pairs (Maximize Affirmed
    Majorities) are monotonic, while Coombs' method, runoff voting and
    instant-runoff voting are not. The single-winner methods of range voting,
    majority judgment and approval voting are also monotonic as one can never
    help a candidate by reducing or removing support for them, but these
    require a slightly different definition of monotonicity as they are not
    preferential systems.

    Of the multiple-winner voting systems, all plurality voting methods are
    monotonic, such as plurality-at-large voting (bloc voting), cumulative
    voting, and the single non-transferable vote. Most versions of the single
    transferable vote, including all variants currently in use for public
    elections (which simplify to instant runoff when there is only one winner)
    are not monotonic.
    """


class IConsistencyCriterion(ICriterion):
    """
    A voting system is consistent if, when the electorate is divided
    arbitrarily into two (or more) parts and separate elections in each part
    result in the same choice being selected, an election of the entire
    electorate also selects that alternative. Smith calls this property
    separability and Woodall calls it convexity.

    It has been proven a preferential voting system is consistent if and only
    if it is a positional voting system. Borda count is an example of this.

    The failure of the consistency criterion can be seen as an example of
    Simpson's paradox.
    """


class IParticipationCriterion(
    """
    The participation criterion is a voting system criterion. It is also known
    as the "no show paradox". It has been defined as follows:

        * In a deterministic framework, the participation criterion says that
          the addition of a ballot, where candidate A is strictly preferred to
          candidate B, to an existing tally of votes should not change the
          winner from candidate A to candidate B.

        * In a probabilistic framework, the participation criterion says that
          the addition of a ballot, where each candidate of the set X is
          strictly preferred to each other candidate, to an existing tally of
          votes should not reduce the probability that the winner is chosen
          from the set X.

    Plurality voting, approval voting, range voting, and the Borda count all
    satisfy the participation criterion.[citation needed] All Condorcet
    methods, Bucklin voting, and IRV fail.

    Voting systems that fail the participation criterion allow a particularly
    unusual strategy of not voting to, in some circumstances, help a voter's
    preferred choice win.

    The participation criterion for voting systems is one example of a rational
    participation constraint for social choice mechanisms in general.
    """


class ICondorcetCriterion(MajorityCriterion):
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


class ICondorcetLoserCriterion(MajorityLoserCriterion):
    """
    In single-winner voting system theory, the Condorcet loser criterion is a
    measure for differentiating voting systems. It implies the majority loser
    criterion.

    A voting system complying with the Condorcet loser criterion will never
    allow a Condorcet loser to win. A Condorcet loser is a candidate who can be
    defeated in a head-to-head competition against each other candidate. (Not
    all elections will have a Condorcet loser since it is possible for three or
    more candidates to be mutually defeatable in different head-to-head
    competitions.)

    A slightly weaker (easier to pass) version is the majority Condorcet loser
    criterion, which requires that a candidate who can be defeated by a
    majority in a head-to-head competition against each other candidate, lose.
    It is possible for a system, such as Majority Judgment, which allows voters
    not to state a preference between two candidates, to pass the MCLC but not
    the CLC.

    Compliant methods include: two-round system, instant-runoff voting,
    contingent vote, borda count, Schulze method, and ranked pairs.
    Noncompliant methods include: plurality voting, supplementary voting, Sri
    Lankan contingent voting, approval voting, range voting, Bucklin voting and
    minimax Condorcet.
    """


class IIndependenceOfIrrelevantAlternativesCriterion(ICriterion):
    """
    In voting systems, independence of irrelevant alternatives is often
    interpreted as, if one candidate (X) wins the election, and a new
    alternative (Y) is added, only X or Y will win the election.

    Approval voting and range voting satisfy the independence of irrelevant
    alternatives criterion. Another cardinal system, cumulative voting, does
    not satisfy the criterion.

    An anecdote which illustrates a violation of this property has been
    attributed to Sidney Morgenbesser:

        After finishing dinner, Sidney Morgenbesser decides to order dessert.
        The waitress tells him he has two choices: apple pie and blueberry pie.
        Sidney orders the apple pie. After a few minutes the waitress returns
        and says that they also have cherry pie at which point Morgenbesser
        says "In that case I'll have the blueberry pie."

    All voting systems have some degree of inherent susceptibility to strategic
    nomination considerations. Some regard these considerations as less serious
    unless the voting system specifically fails the (easier to satisfy)
    independence of clones criterion.
    """


class IIndependenceOfClonesCriterion(ICriterion):
    """
    In voting systems theory, the independence of clones criterion measures an
    election method's robustness to strategic nomination. Nicolaus Tideman
    first formulated the criterion, which states that the addition of a
    candidate identical to one already present in an election will not cause
    the winner of the election to change.

    In some systems, the introduction of a clone tends to divide support
    between the similar candidates, worsening all their chances. In some other
    systems, the presence of a clone tends to reduce support for dissimilar
    candidates, improving the chances of one (or more) of the similar
    candidates. In yet other systems, the introduction of clones does not
    significantly affect the chances of similar candidates. There are further
    systems where the effect of the introduction of clones depends on the
    distribution of other votes.

    Elections methods that fail independence of clones can either be clone
    negative (the addition of an identical candidate decreases a candidate’s
    chance of winning) or clone positive (the reverse). The Borda count is an
    example of a clone positive method. Plurality is an example of a clone
    negative method because of vote-splitting.

    Instant-runoff voting, approval voting and range voting meet the
    independence of clones criterion. Some election methods that comply with
    the Condorcet criterion such as Ranked pairs and Schulze[2] also meet
    independence of clones.

    The Borda count, Minimax, two-round system, Bucklin voting and plurality
    fail the independence of clones criterion.
    """


class IReversalSymmetryCriterion(ICriterion):
    """
    Reversal symmetry is a voting system criterion which requires that if
    candidate A is the unique winner, and each voter's individual preferences
    are inverted, then A must not be elected. Methods that satisfy reversal
    symmetry include Borda count, the Kemeny-Young method, and the Schulze
    method. Methods that fail include Bucklin voting, instant-runoff voting and
    Condorcet methods that fail the Condorcet loser criterion such as Minimax.

    For cardinal voting systems which can be meaningfully reversed, approval
    voting and range voting satisfy the criterion.
    """


class IPolynomialTimeCriterion(ICriterion):
    """
    Can the winner be calculated in a runtime that is polynomial in the number
    of candidates and the number of voters?

    Problems for which a polynomial time algorithm exists belong to the
    complexity class IP, which is central in the field of computational
    complexity theory. Cobham's thesis states that polynomial time is a synonym
    for "tractable", "feasible", "efficient", or "fast".
    """


class ISummabilityCriterion(ICriterion):
    """
    How much information must be transmitted from each polling station to a
    central location in order to determine the winner?

    This is expressed as an order function of the number of candidates N.
    Slower-growing functions such as O(N) or O(N2) make for easier counting,
    while faster-growing functions such as O(N!) might make it harder to catch
    fraud by election administrators.
    """


class IAllowsEqualRankingsCriterion(ICriterion):
    """
    Can a voter choose whether to rank any two candidates equally at any
    position on the ballot?

    This can reduce the prevalence of spoiled ballots due to overvotes, and can
    give a less-dishonest alternative to some tactical voting strategies.
    """


class IAllowsLaterPreferencesCriterion(ICriterion):
    """
    Can a voter indicate different levels of support through ranking or rating
    candidates?
    """


class ILaterNoHarmCriterion(ICriterion):
    """
    The later-no-harm criterion is a voting system criterion formulated by
    Douglas Woodall. The criterion is satisfied if, in any election, a voter
    giving an additional ranking or positive rating to a less preferred
    candidate cannot cause a more preferred candidate to lose.

    Single transferable vote (including Instant Runoff Voting and Contingent
    vote), Minimax Condorcet (pairwise opposition variant which does not
    satisfy the Condorcet Criterion), and Descending Solid Coalitions, a
    variant of Woodall's Descending Acquiescing Coalitions rule, satisfy the
    later-no-harm criterion.

    However, if a method permits incomplete ranking of candidates, and if a
    majority of initial round votes is required for election, it cannot satisfy
    Later-no-harm, because a lower preference vote cast may create a majority
    for that lower preference, whereas if the vote was not cast, the election
    could fail, proceed to a runoff, repeated ballot or other process, and the
    favored candidate could possibly win.

    Approval voting, Borda count, Range voting, Schulze method and Bucklin
    voting do not satisfy later-no-harm. The Condorcet criterion is
    incompatible with later-no-harm.

    When Plurality is being used to fill two or more seats in a single district
    (Plurality-at-large) it fails later-no-harm.

    The later-no-harm criterion is by definition inapplicable to any voting
    system in which a voter is not allowed to express more than one choice,
    including plurality voting, the system most commonly used in Canada, India,
    the UK, and the USA.
    """
