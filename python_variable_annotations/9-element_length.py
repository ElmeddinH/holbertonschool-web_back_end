#!/usr/bin/env python3
"""Module for element_length function with type annotations."""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return list of tuples with elements and their lengths."""
    return [(i, len(i)) for i in lst]
