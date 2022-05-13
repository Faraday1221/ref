ratings = [1,2,87,87,87,2,1]
# [1,2,3,1,3,2,1]

def update(ratings, score, i, j):
    if ratings[i] > ratings[j] and score[i] <= score[j]:
        score[i] = score[j] + 1
    elif ratings[j] > ratings[i] and score[j] <= score[i]:
        score[j] = score[i] + 1
    return score

score = [1 for _ in ratings]

print("forwards pass")
for j in range(1, len(ratings)):
    score = update(ratings, score, i=j-1, j=j)
    print(score)
print("backwards pass")
for j in range(len(ratings)-1,0,-1):
    # print(j,j-1)
    score = update(ratings, score, j=j, i=j-1)
    print(score)

print(sum(score))


# score = [1 for _ in ratings]

# for j in range(1,len(ratings)):
#     i = j - 1
#     if ratings[j] > ratings[i]:
#         score[j] += 1
#     elif ratings[i] > ratings[j]:
#         if not score[i] > score[j]:
#             score[i] += 1

# print(sum(score))

# =================================================================
#	Submitted solution
# =================================================================
# NOTE moving update into candy as inline code is a 50% speed up
def update(ratings: List[int], score: List[int], i:int, j:int) -> List[int]:
    if ratings[i] > ratings[j] and score[i] <= score[j]:
        score[i] = score[j] + 1
    elif ratings[j] > ratings[i] and score[j] <= score[i]:
        score[j] = score[i] + 1
    return score

class Solution:
    def candy(self, ratings: List[int]) -> int:
        score = [1 for _ in ratings]

        print("forwards pass")
        for j in range(1, len(ratings)):
            score = update(ratings, score, i=j-1, j=j)
        print("backwards pass")
        for j in range(len(ratings)-1,0,-1):
            score = update(ratings, score, j=j, i=j-1)

        return sum(score)