
def foo(nums1, m, nums2, n):
    # convert to python zero idx
    m -= 1
    n -= 1

    size = len(nums1)
    idx = size - 1
    out = [0 for _ in range(size)]
    for i in range(size):
        if m < 0:
            val1 = 0
        else:
            val1 = nums1[m]
        # set val2 to zero if nums2 is empty
        if n < 0 or not nums2:
            val2 = 0
        else:
            val2 = nums2[n]
        
        print(f"val1={val1}, val2={val2}, m={m}, n={n}")
        # -----
        if n < 0 or not nums2:
            nums1[idx - i] = val1
            m = m -1
        elif m < 0:
            nums1[idx - i] = val2
            n = n -1
        # -----
        # has trouble selecting a value when they are equal
        elif val1 > val2:
            nums1[idx - i] = val1
            m = m - 1
        elif val1 < val2:
            nums1[idx - i] = val2
            n = n - 1
        # else take from which ever array has more values
        elif val1 == val2:
            nums1[idx  - i] = val1
            if n >= m:
                n = n -1
            else:
                m = m -1

        print(f"nums1 = {nums1}")
    return nums1

# here is an example where zeros are just terrible
foo(
nums1=[0,0,3,0,0,0,0,0,0],
n=3,
nums2=[-1,1,1,1,2,3],
m=6,
)
# expected [-1,0,0,1,1,1,2,3,3]
# actual [0,0,-1,1,1,1,2,3,3]

foo(
    nums1=[-1,0,0,3,3,3,0,0,0],
n=6,
nums2=[1,2,2],
m=3,
)
# actual [0,0,0,1,2,2,3,3,3]
# expected [-1,0,0,1,2,2,3,3,3]

foo(
nums1 = [1],
nums2 = [],
m = 1,
n = 0,
)

foo(
nums1 = [1,2,3,0,0,0],
nums2 = [2,5,6],
m=3,
n = 3,
)

foo(
nums1 =[0],
nums2=[1],
m=0,
n=1,
)

foo(
nums1 = [2,0],
nums2 = [1],
n=1,
m = 1,
)

foo(
    nums1=[-1,0,0,3,3,3,0,0,0],
    n=6,
    nums2=[1,2,2],
    m=3,
)

def bar(nums1, m, nums2, n):

    size = n + m
    for i in range((size -1), -1, -1):
        print(i)
        if n <= 0:
            print("you are here...")
            break
        if (m <= 0) or (nums2[n-1] > nums1[m -1]):
            nums1[i] = nums2[n-1]
            n = n - 1
        else:
            nums1[i] = nums1[m-1]
            m = m - 1
        print(nums1)

bar(
    nums1=[-1,0,0,3,3,3,0,0,0],
    m=6,
    nums2=[1,2,2],
    n=3,
)