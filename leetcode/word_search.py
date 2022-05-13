# board = [["A","B","E"],["S","F","C"],["A","B","C"]]
# word = "ABC"

# board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
# word = "ABCCED"

# board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
# word = "SEE"

board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "ABCB"

def base(board, word):
    """get the base coordinates to start a search"""
    m, n = len(board), len(board[0])
    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0]:
                yield (i,j)

def adjacent(i,j,board, stack):
    m, n = len(board), len(board[0])
    if i - 1 > -1 and (i-1,j) not in stack:
        yield (i-1,j)
    if i + 1 < m and (i+1,j) not in stack:
        yield (i+1,j)
    if j - 1 > -1 and (i,j-1) not in stack:
        yield (i,j-1)
    if j + 1 < n and (i,j+1) not in stack:
        yield (i,j+1)

def descend_tree(i,j,board,stack,word):
    print(f"start descend tree. stack={stack}. letters={[board[a][b] for a,b in stack]}")
    for ii, jj in adjacent(i,j,board,stack):
        if len(stack) == len(word): break
        print(f"checking {(ii,jj)}... letter={board[ii][jj]}")
        if board[ii][jj] == word[len(stack)]:
            stack.append((ii,jj))

            if len(stack) == len(word):
                print('='*30)
                print(f"FOUND MATCH: stack={stack}")
                print([board[a][b] for a,b in stack])
                print('='*30)
                break

            descend_tree(ii,jj,board,stack,word)

    if not len(stack) == len(word):
        print("no match found... pop stack")
        stack.pop()
    return stack


# =================================================================
#	script
# =================================================================
print("Board:")
for line in board:
    print(line)
print('-'*30)
print(f"Match Word: {word}")
print('-'*30)
stack = []

for i,j in base(board, word):
    if len(stack) == len(word): break
    stack.append((i,j))
    print((i,j))
    stack = descend_tree(i,j,board, stack,word)
    print(f"FINAL STACK: {stack}")

print("\n")
if len(stack) == len(word):
    print("MATCH FOUND")
else:
    print("NO MATCH FOUND")