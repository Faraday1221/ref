# look at each char in s
# if opening bracket add to stack
# if closing bracket and stack not empty
#    if match stack[-1] pop from stack
#    else return false
# if stack is empty return true else false


def foo(s):
    pairs = {"{": "}", "[": "]", "(": ")"}
    stack = []

    for c in s:
        # if opening bracket add to stack
        if c in pairs.keys():
            stack.append(c)
        # if closing bracket
        elif len(stack) > 0:
            # matches stack pop the last stack item
            if c == pairs[stack[-1]]:
                _ = stack.pop()
            else:
                # if mismatch i.e. { & ] is invalid
                return False
        else:
            return False

    # true iff the stack isn't empty
    return len(stack) == 0
