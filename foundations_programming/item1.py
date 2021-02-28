from typing import NamedTuple
from collections import Counter, defaultdict

# https://techdevguide.withgoogle.com/paths/foundational/find-longest-word-in-dictionary-that-subsequence-of-given-string/#!
S = "abppplee"
D = ["able", "ale", "apple", "bale", "kangaroo"]

# since the same letters are grouped together this gets easier
class Profile(NamedTuple):
    length: int
    ele: set
    counter: Counter
    idx: dict

# capture the earliest index of a letter in the reference str
idx = {}
for n, letter in enumerate(S):
    if letter not in idx:
        idx[letter] = n

source = Profile(length=len(S), counter=Counter(S), idx=idx, ele=set(S))

for word in D:

    foo = False

    if len(word) > source.length:
        print(f"{word}: FAIL len")
        foo = True
        pass
    if set(word).issubset(source.ele):
        word_cnt = Counter(word)
        for letter, cnt in word_cnt.items():
            if source.counter[letter] < cnt:
                print(f"{word}: FAIL too many letters")
                foo = True
                pass

        for i in range(len(word) - 1):
            if source.idx[word[i]] > source.idx[word[i + 1]]:
                print(f"{word}: FAIL wrong order")
                foo = True
                pass

        if not foo:
            print(word)

    # NOTE: this should ultimately grab the longest word



# =================================================================
#	Replicate Counter...
# =================================================================
# getting a few reps in with some common collections

letter_cnt = Counter(S)
# Counter({'a': 1, 'b': 1, 'p': 3, 'l': 1, 'e': 2})

# with defaultdict
defdic_letter_cnt = defaultdict(int)
for letter in S:
    defdic_letter_cnt[letter] += 1
# defaultdict(int, {'a': 1, 'b': 1, 'p': 3, 'l': 1, 'e': 2})

# from scratch
scratch_letter_cnt = {k: 0 for k in S}
for letter in S:
    scratch_letter_cnt[letter] += 1
# {'a': 1, 'b': 1, 'p': 3, 'l': 1, 'e': 2}