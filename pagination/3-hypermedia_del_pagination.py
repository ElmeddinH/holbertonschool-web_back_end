#!/usr/bin/env python3
"""Module for deletion-resilient hypermedia pagination."""
import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize Server with no cached dataset or indexed dataset."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset loaded from CSV file."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:
        """Return deletion-resilient pagination info for the given index."""
        indexed = self.indexed_dataset()
        assert isinstance(index, int) and 0 <= index < len(self.dataset())
        data = []
        current = index
        while len(data) < page_size:
            if current in indexed:
                data.append(indexed[current])
            current += 1
        return {
            "index": index,
            "data": data,
            "page_size": len(data),
            "next_index": current
        }
