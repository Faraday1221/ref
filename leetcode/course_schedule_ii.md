# Course Schedule ii
 https://leetcode.com/problems/course-schedule-ii/

## Key Concept: Adjacency List
In order to represent a graph we can use an adjacency list i.e.
```py
# adjacency list
# keys are verticies and values are adjacent verticies
# direction is implied i.e. 0 points to 1 and 2
# the graph would be 0 -> 1 -> 3 and 0 -> 2 -> 3
foo = {
    0: [],
    1: [0],
    2: [0],
    3: [1,2],
}
```

## Key Concept: Topological Sort
The algorithm is explained very well [here](https://www.interviewcake.com/concept/java/topological-sort). 

This is a common algorithm design pattern:
1. Figure out how to get the first thing.
1. Remove the first thing from the problem.
1. Repeat.

Here the first thing to find is the node with no dependencies. *If all nodes have dependencies, something is circular and the graph is not acyclic*.