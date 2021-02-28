# 1.4
from typing import List
import logging

# set to debug to see 'print' statements
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


T = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
U = [1, 2, 3, 4, 5, 6]
V = [6, 5, 4, 3, 2, 1]


# =================================================================
#	Problem 1.4.1
# =================================================================

# NOTE the book goes on to describe how these two algorithms
# perform very differently given the properties of the input arrays
# in the worst case both perform in quadratic time
# TODO how do i calculate that this is quadratic time?

def insert(T: List[int]) -> List[int]:
    """best case, the list is sorted: touch each element once, n operations
    worse case, list is reverse sorted: sum(1:n) operations loop_cnt = (sum(1:n-1))"""
    operations = 0
    for i, x in enumerate(T):
        j = i - 1
        operations += 1
        while j > -1 and x < T[j]:
            T[j + 1] = T[j]
            j = j - 1
            operations += 1
        T[j + 1] = x
    logging.debug(operations)
    return T


def select(T: List[int]) -> List[int]:
    """the order of the sorted list doesn't matter here
    i.e. cnt of operations for U and V are identical
    as opposed to insert where U has 6 operations and V has 21"""
    operations = 0
    for i in range(len(T)-1):
        minj = i
        minx = T[i]
        operations += 1
        for j in range(i+1, len(T)):
            operations += 1
            if T[j] < minx:
                minj = j
                minx = T[j]
        T[minj] = T[i]
        T[i] = minx
    logging.debug(operations)
    return T


# def _insert_worst_case(N: int) -> int:
#     """worse case number of operations for insert given N elements"""
#     return sum([i+1 for i in range(N)])

# def _select_worst_case(N: int) -> int:
#     pass

# =================================================================
#	Problem 1.5.1 **
# =================================================================
# TODO this is an involved problem... come back to it later

# =================================================================
#	Problem 1.7.1
# =================================================================
# the efficency of the algorith is based on the 'word' size of 'a' and 'b'.
# where 'word' means length of the representation in decimal or binary

# TODO i cannot figure out how to caluclaute the additional time.
# i see that its longer, and why but i'm lost with how to put a figure to the time

# I see that when m > n the number of operations increases by a factor of m/n
# i.e. n,m = 5,13 this results in 16 operations. n,m=13,5 there are 42 operations
# which is ~= 13/5 * 16
def russe(a: int, b: int) -> int:
    """russe multiplication of a and b
    a: multiplier, the number that divides by 2 each time
    b: multiplicand, thnoe number that is multipled by 2 each time"""
    x: list = [a]
    y: list = [b]
    i = 0
    operations = 0
    while x[i] > 1:
        x.append(x[i] // 2)
        y.append(y[i] + y[i])
        i += 1
        logging.debug(f"i={i}, x={x}, y={y}")
        operations += 2
    # sum only odd numbers
    prod = 0
    while i >= 0:
        if x[i] % 2 != 0:
            prod += y[i]
            operations += 1
        logging.debug(f"i={i}, prod={prod}")
        i -= 1
        operations += 1
    logging.debug(f"{operations} operations")
    logging.debug(f"bit length: m={a.bit_length()}, n={b.bit_length()}")
    return prod

# a, b = 45, 1945

def gcd(m: int, n: int) -> int:
    """greatest common denominator"""
    a,b = (m,n) if m < n else (n,m)
    for i in range(a):
        if a % (a - i) == 0 and b % (a - i) == 0:
            return a - i
    return 1

def euclid(m: int, n: int) -> int:
    """log n efficient algorithm to find gcd"""
    while m > 0:
        t = n % m
        n = m
        m = t
    return n

def fib(n: int) -> int:
    f0, f1 = 0, 1
    operations = 1
    for _ in range(n):
        f1 += f0
        # logging.debug(f1)
        f0 = f1
        operations += 1
        logging.debug(f"operations: {operations}")
    return f1
        