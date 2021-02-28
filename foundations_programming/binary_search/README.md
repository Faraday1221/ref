## Binary Search
This repo contains my notes from the real-python binary search tutorial. [source code](https://github.com/realpython/materials/tree/master/binary-search).

*I attempted to write my own binary search algorithm, and found it was challenging, hence going through this tutorial. The tutorial dives into some additional concepts like, linear search, binary search and benchmarking... the repo code is high quality, and worth a look!*

### Grab Data
Download the source data and cache two files, `names.txt` and `sorted_names.txt`. 

```sh
# creates names.txt and sorted_names.txt
python3 download_imdb.py
```

### Search from Scratch
There was plenty of goodness to reviewing the code in this tutorial; especially with typing. So I'm going to try and replicate it and see what I've internalized.

#### Seperate Index from Retrieve Element
The implementation used is about seperating finding an index value from returning the actual element. *This ties in pretty well with the idea that search is about WHERE as well as WHAT*.

##### Generic TypeVar
A big part of the learning here is about Generic TypeVar [docs](https://mypy.readthedocs.io/en/latest/generics.html#generics) & [PEP484](https://www.python.org/dev/peps/pep-0484/#user-defined-generic-types). The big take away here is **typing can't infer type in a sequence, generic TypeVar is to explicitly show how the sequence type tracks through the function**. e.g.

```py
from typing import Sequence, TypeVar, Optional

T = TypeVar("T")

def foo(elements: Sequence[T], value: T) -> Optional[T]:
    """T shows how the element is related to elements, value and return val"""
    pass
```