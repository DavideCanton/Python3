__author__ = 'davide'

import collections
import re
import random
import string


def verify(regex, winners, losers):
    """Verify that regex matches all winners but no losers."""
    missed_winners = {w for w in winners if not re.search(regex, w)}
    matched_losers = {L for L in losers if re.search(regex, L)}
    if missed_winners:
        print("Error: should match but did not:", ', '.join(missed_winners))
    if matched_losers:
        print("Error: should not match but did:", ', '.join(matched_losers))
    return not (missed_winners or matched_losers)


def findregex(winners, losers, tries=100):
    """Find a regex that matches all winners
    but no losers (sets of strings)."""
    # Precompute a pool of component regexes,
    # and a cache of {regex: winners}.
    # Make a pool of regex components, then
    # pick from them to cover winners.
    # Call 'findregex1' repeatedly ('tries' times),
    # and pick the shortest result.
    pool, cache = precompute_regex_components(winners, losers)
    print("Precomputed...")
    candidate_regexes = [findregex1(winners, pool, cache)
                         for _ in range(tries)]
    return min(candidate_regexes, key=len)


def precompute_regex_components(winners, losers):
    """Return a pool of regexes, and a cache of {regex: {winner...}}."""
    pool = regex_components(winners, losers)
    cache = eliminate_dominated({c: matches(c, winners) for c in pool})
    return set(cache), cache


def findregex1(winners, pool, cache):
    """Find a regex that matches all winners but no
    losers (sets of strings)."""
    # On each iteration, add the 'best' component to 'cover',
    # remove winners covered by best, and keep in 'pool' only components
    # that still match some winner. The score function has some randomness.
    winners, pool, cache = winners.copy(), pool.copy(), cache.copy()
    cover = []

    def matches2(regex, strings):
        return {w for w in cache[regex] if w in strings}

    K = random.choice([3, 4, 4, 5, 6])

    def score(c):
        return K * len(matches2(c, winners)) - len(c) + random.random()

    while winners:
        best = max(pool, key=score)
        cover.append(best)
        winners -= cache[best]
        pool.difference_update({c for c in pool if not matches2(c, winners)})
    return '|'.join(cover)


def eliminate_dominated(cache):
    """Given a cache of {regex: {winner...}}, eliminate from cache all
    regexes dominated
    by another: R1 is dominated by R2 if R2 covers a superset of R1, and R2
    is shorter."""
    # First make a dict that is the inverse of cache: {winner: {regex...}}
    invcache = invert_multimap(cache)
    return {r1: cache[r1]
            for r1 in cache if not dominated(r1, cache, invcache)}


def dominated(r1, cache, invcache):
    """r1 is dominated if there is some r2 that dominates it."""
    candidate_dominators = {r2 for winner in cache[r1] for r2 in
                            invcache[winner]
                            if r2 != r1}
    return any(dominates(r2, r1, cache) for r2 in candidate_dominators)


def dominates(r2, r1, cache):
    """r2 dominates r1 if they cover the same and r2 has fewer characters,
    or if r2 covers a superset and has fewer or the same number of
    characters."""
    if cache[r1] == cache[r2]:
        return (len(r2), r2) <= (len(r1), r1)
    else:
        return (cache[r2] > cache[r1]) and (len(r2) <= len(r1))


def invert_multimap(multimap):
    """Given a dict of {key: {val...}}, return a dict of {val: {key...}}."""
    result = collections.defaultdict(set)
    for key in multimap:
        for val in multimap[key]:
            result[val].add(key)
    return result


def regex_components(winners, losers):
    """Return components that match at least one winner, but no loser."""
    wholes = {'^' + winner + '$' for winner in winners}
    parts = {d for w in wholes for p in subparts(w) for d in dotify(p)}
    reps = {s for p in (parts | winners) for s in repetitions(p)}
    return wholes | {p for p in (parts | reps)
                     if not any(re.search(p, loser) for loser in losers)}


def repetitions(part):
    """Insert a repetition character ('+' or '*' or '?')
    after each non-special character."""
    return {"{}{}{}".format(A, rep, B) for (A, B) in splits(part)
            # Don't allow '^*' nor '$*' nor '..*' nor '.*.'
            if not A[-1] in '^$'
            if not A.endswith('..')
            if not (A.endswith('.') and B.startswith('.'))
            for rep in '?'}  # +*?


def splits(part):
    """All ways to split part into two pieces, where the first is non-empty."""
    return [(part[:i], part[i:]) for i in range(1, len(part) + 1)]


def subparts(word):
    """Return a set of subparts of word, consecutive
    characters up to length 4."""
    max_length = len(word)
    return {word[i:i + n] for i in range(len(word))
            for n in range(1, max_length + 1)}


def dotify(part):
    """Return all ways to replace a subset of chars in part with '.'."""
    if part == '':
        return {''}
    else:
        return {c + rest for rest in dotify(part[1:])
                for c in replacements(part[0])}


def replacements(char):
    """Return possible replacement characters for char
    (char + '.' unless char is special)."""
    return char if char in '^$' else char + '.'


def matches(regex, strings):
    """Return a set of all the strings that are matched by regex."""
    return {s for s in strings if re.search(regex, s)}


winners = set('''washington adams jefferson jefferson madison madison monroe
monroe adams jackson jackson vanburen harrison polk buchanan
lincoln lincoln grant hayes garfield harrison
mckinley taft wilson wilson harding coolidge hoover roosevelt
roosevelt truman eisenhower eisenhower kennedy johnson nixon
nixon carter reagan reagan bush clinton clinton bush
bush obama obama'''.split())

losers = set('''clinton jefferson adams pinckney pinckney clinton king adams
jackson adams clay vanburen vanburen clay cass scott fremont breckinridge
mcclellan seymour greeley tilden hancock blaine cleveland harrison bryan bryan
parker bryan roosevelt hughes cox davis smith hoover landon wilkie dewey dewey
stevenson stevenson nixon goldwater humphrey mcgovern ford carter mondale
dukakis bush dole gore kerry mccain romney'''.split())
losers = losers - winners


def random_word_set():
    l = random.randint(3, 15)
    return {"".join(random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(3, 10)))
            for _ in range(l)}


if __name__ == "__main__":
    winners = random_word_set()
    losers = random_word_set()
    losers -= winners

    print(winners)
    print(losers)
    answer = findregex(winners, losers)
    print(answer, len(answer))
    if verify(answer, winners, losers):
        print("Soluzione corretta.")
    else:
        print("No!")
