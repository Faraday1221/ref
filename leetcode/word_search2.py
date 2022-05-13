
m, n = len(board), len(board[0])

stack = []
visited = ()

def adjacent(board, i, j, visited):
    adj = []
    if i-1 >= 0 and (i-1, j) not in visited:
        adj.append(i-1,j)
    if i+1 < len(board) and (i+1, j) not in visited
        adj.append(i+1, j)
    if j-1 >= 0 and (i, j-1) not in visited
        adj.append(i,j-1)
    if j+1 < len(board[0]) and (i,j+1) not in visited:
        adj.append(i, j+1)
    return adj

def dfs(i, j, board, stack, visited):
    node = board(i,j)
    if node not in visited:
        print((i,j), board[i][j])
        visited.add(node)
        for ii, jj in adjacent(board, i, j, visited):
            


for i in range(m):
    for j in range(n):

