#!/usr/bin/env python3
"""Module for to_kv function with type annotations."""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Return a tuple of string and square of int/float."""
    return (k, float(v * v))
