## Foundations of Programming
My notes from [this course](https://techdevguide.withgoogle.com/paths/foundational/find-longest-word-in-dictionary-that-subsequence-of-given-string/#!)

#### Problem 1
There is quite a bit of depth to the big-O discussion of this problem. *There is plenty of interesting considerations to this problem; its worth returning to this with fresh eyes.* [source code](./item1.py)

#### Skipped Problems (all Java)
- #2 Java String Tutorial
- #3 Java Array Tutorial
- 5, 6, 7, 8

#### Problem 4
This problem as posted is for Java [here is the python version](https://codingbat.com/prob/p118366).
```py
def string_splosion(string):
    return "".join([string[:n+1] for n in range(len(string))])
```

#### Problem 5
There is no python equivolent, but [this problem was close](https://codingbat.com/prob/p108886).

```py
def sum67(nums):
    counter = [0]
    skip = False

    for n in nums:
        if n == 6:
            skip = True
        if not skip:
            counter.append(n)
        if n == 7:
            skip = False
    return sum(counter)

```

*If we were doing the MaxSpan problem, we could find a list of all index values for all numbers in the array, then calculate the max distance between th index numbers*
```py
from collections import defaultdict
from operator import itemgetter

array = [1,1,2,3,4,5,1,2,2,1,4,5,1]

holder = defaultdict(list)
for idx, ele in enumerate(array):
    holder[ele].append(idx)

# defaultdict(list,
#             {1: [0, 1, 6, 9, 12],
#              2: [2, 7, 8],
#              3: [3],
#              4: [4, 10],
#              5: [5, 11]})
span = {k: max(v) - min(v) for k, v in holder.items()}
# {1: 12, 2: 6, 3: 0, 4: 6, 5: 6}
max_ele, max_span = max(span.items(), key=itemgetter(1))
# (1, 12)
```

#### Problem 6
*Another Java problem with no Python analog... here is the python solution anyway*.

```py
import regex as re

def withoutString(sentence, sub_word):
    return re.sub(f"[{sub_word}]","", sentence)

# withoutString("Hello there", "llo") → "He there"
# withoutString("Hello there", "e") → "Hllo thr"
# withoutString("Hello there", "x") → "Hello there"
```
#### Problem 7
*Another Java problem with no Python...*
```py
import string

def didnt_read_carefully(chars):
    # this doesnt conform to the expectations i.e. 11abc22 -> 33
    return sum([int(c) for c in chars if c not in string.ascii_letters])

def solution(chars):
    # chars = '11abc22'
    holder = [c if c.isdigit() else "," for c in chars]
    # ['1', '1', ',', ',', ',', '2', '2']
    nums = [int(i) for i in "".join(holder).split(",")]
    # [11, 22]
    return sum(nums)
```
#### Problem 8
*all Java no python...*
this is an interesting problem... the arrays are so small its easy to brute force step through and calculate left_sum, right_sum.

...the efficient solution is to binary search! **Below is a hacky binary search** *(that apparently doesn't work... but there is plenty of learning opportunity here!)* [check out this article when there is time](https://realpython.com/binary-search-python/)

```py
from typing import Optional

def mid(x: list) -> int:
    return round(len(x)/2)

def get_new_idx(left: list, right: list, current_idx: int) -> int:
    #step to the half way point of the right array
    if sum(left) < sum(right): 
        mid_idx = current_idx + mid(right)
    # step the the half way point of the left array
    else:
        mid_idx = mid(left)
    return mid_idx

def binary_search(ex: list, mid_idx: Optional[int]= None) -> int:
    # HACK to control recursion depth
    global counter
    counter +=1
    # print(f"cnt: {counter}")
    if counter > len(ex)+1:
        print("No Solution")
        counter = 0
        return 0

    if mid_idx is None:
        mid_idx = mid(ex)
    print("idx", mid_idx)
    # split array into left, right
    left, right = ex[:mid_idx], ex[mid_idx:]
    print(left, right)
    print(sum(left), sum(right))
    if sum(left) == sum(right):
        print(f"solution found: idx={mid_idx}")
        return mid_idx
    else:
        new_idx = get_new_idx(left, right, mid_idx)
        binary_search(ex, mid_idx=new_idx)

ex = [1,2,3,4,5,6,7,2]

# NOTE this has the fatal problem of continuing forever if the problem doesn't converge
# e.g. [1,2,3,4,5,6,7,2,1] will bounce between idx 3 and 6 forever 
# one hack to stop this is to record all "seen" idx and if a value is repeated stop
# another idea - which isn't great it to ensure that no matter what we do not check
# more than N indicies when we have an array of N values e.g. no worse than brute force
# we know binary search is log(N) so if we have more than log(N) guesses - stop

# HACK added a parent function that tracks recursion and will error on a non-solution

# HACK apparnetly this DOES NOT quite work as intended...
# fails on the first test case... jumps between idx 2 and 4 only!
# i.e. my split algorithm is wrong :P
# binary_search([1, 1, 1, 2, 1]) → true (FAIL)
# binary_search([2, 1, 1, 2, 1]) → false (PASS)
# binary_search([10, 10]) → true (PASS)
```