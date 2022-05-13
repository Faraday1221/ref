# https://leetcode.com/problems/course-schedule-ii/
# Return the ordering of courses you should take to finish all courses
# prerequisites_i = a_i, b_i
# b_i must be completed before a_i
from typing import NamedTuple, List


class Case(NamedTuple):
    numCourses: int
    prerequisites: List[List[int]]
    output: list


testcases = [
    # example 1
    Case(numCourses=2, prerequisites=[[1, 0]], output=[0, 1]),
    # example 2
    Case(
        numCourses=4,
        prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]],
        output=[[0, 2, 1, 3], [0, 1, 2, 3]],
    ),
    # example 3
    Case(
        numCourses=1,
        prerequisites=[],
        output=[0],
    ),
    # made up test case to fail
    Case(numCourses=2, prerequisites=[[0, 1], [1, 0]], output=[]),
    # failed test case
    Case(numCourses=3, prerequisites=[[1, 0], [1, 2], [0, 1]], output=[]),
]


# =================================================================
#	scratch pad
# =================================================================
# create adjacency list
# i.e. turn prerequisites into foo
# foo = {
#     0: [],
#     1: [0],
#     2: [0],
#     3: [1,2],
# }

N = 0
c = testcases[N]
numCourses = c.numCourses
prerequisites = c.prerequisites
print(f"Expected: {c.output}")

# convert the input to look like an adjacency list
foo = {n: [] for n in range(numCourses)}
for c, d in prerequisites:
    foo[c].append(d)

# def remove_from_foo(foo, k):
#     # remove k from all other lists
#     print("bottom loop")
#     print(f"foo={foo}")
#     for k_, v_ in foo.items():
#         # if the matched item
#         if k in v_:
#             print(f"pop k={k}, before: v_={v_}")
#             foo[k_] = [i for i in v_ if i != k]
#             print(f"after v_={v_}")
#     return foo

print(f"foo={foo}")
# find the first key with an empty list
# add that value to our sorted list
# remove that value from all other lists
bar = []
for _ in range(numCourses):
    print(f"{_} top loop")
    print(f"bar={bar}")
    print(f"foo={foo}")
    for k, v in foo.items():
        if not v:
            print(f"k={k}, v={v}")
            bar.append(k)
            del foo[k]
            # foo = remove_from_foo(foo, k)
            for k_, v_ in foo.items():
                # if the matched item
                if k in v_:
                    print(f"pop k={k}, before: v_={v_}")
                    foo[k_] = [i for i in v_ if i != k]
                    print(f"after v_={v_}")
            break
if foo:
    bar = []


print(f"bar={bar}")

# =================================================================
# 	submission for leetcode
# =================================================================
def remove_k_from_foo(foo, k):
    # remove k from all other lists
    for k_, v_ in foo.items():
        if k in v_:
            foo[k_] = [i for i in v_ if i != k]
    return foo


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        foo = {n: [] for n in range(numCourses)}
        for c, d in prerequisites:
            foo[c].append(d)

        bar = []
        for _ in range(numCourses):
            for k, v in foo.items():
                if not v:
                    bar.append(k)
                    del foo[k]
                    foo = remove_k_from_foo(foo, k)
                    break
        # if foo isn't empty there is a circular dependency
        if not foo:
            return bar
        else:
            return []
