import random
from typing import Sequence, Optional, TypeVar

from search import T, S

# NOTE: since value doesn't *have* to be an element in sequence
# i.e. the original code uses elements: Sequence[T], value: S

def find_index(elements: Sequence[T], value: S) -> Optional[int]:
    checked = set()
    n_elements = len(set(elements))
    while True:
        # randomly select an element from a sequence
        idx = random.choice(range(n_elements))
        # keep track of all elements selected
        checked.add(idx)
        # see if the element selected matches the user search value
        if elements[idx] == value:
            return idx

        checked.add(idx)
        if len(checked) == n_elements:
            # if all selected stop
            return None

def find(elements: Sequence[T], value: S) -> Optional[T]:
    idx = find_index(elements, value)
    return elements[idx] if idx is not None else None