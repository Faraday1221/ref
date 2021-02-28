# https://www.python.org/dev/peps/pep-0484/#user-defined-generic-types
from typing import TypeVar

T = TypeVar("T")
S = TypeVar("S")

# in the tutorial there is an "identity function"
# i believe it is used primarily as another form of typing
# where the identity function is as the 'key' function 
# that extracts and returns an element from several different types