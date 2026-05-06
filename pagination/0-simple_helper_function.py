#!/usr/bin/env python3
"""Module for simple pagination helper function."""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return a tuple of start and end indexes for the given pagination params.

    Page numbers are 1-indexed, so page 1 starts at index 0.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)
