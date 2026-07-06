import pytest
from main import paginate_list


class TestPaginateList:
    def test_nopager_returns_all_items(self):
        items = [1, 2, 3, 4, 5]
        result = paginate_list(items, page=1, page_size=2, nopager=True)
        assert result == [1, 2, 3, 4, 5]

    def test_first_page(self):
        items = [1, 2, 3, 4, 5]
        result = paginate_list(items, page=1, page_size=2, nopager=False)
        assert result == [1, 2]

    def test_second_page(self):
        items = [1, 2, 3, 4, 5]
        result = paginate_list(items, page=2, page_size=2, nopager=False)
        assert result == [3, 4]

    def test_last_partial_page(self):
        items = [1, 2, 3, 4, 5]
        result = paginate_list(items, page=3, page_size=2, nopager=False)
        assert result == [5]

    def test_page_beyond_range_returns_empty(self):
        items = [1, 2, 3]
        result = paginate_list(items, page=10, page_size=2, nopager=False)
        assert result == []

    def test_empty_list(self):
        result = paginate_list([], page=1, page_size=10, nopager=False)
        assert result == []

    def test_page_zero_treated_as_one(self):
        items = [1, 2, 3, 4, 5]
        result = paginate_list(items, page=0, page_size=2, nopager=False)
        assert result == [1, 2]

    def test_negative_page_treated_as_one(self):
        items = [1, 2, 3, 4, 5]
        result = paginate_list(items, page=-1, page_size=2, nopager=False)
        assert result == [1, 2]

    def test_page_size_one(self):
        items = [1, 2, 3]
        result = paginate_list(items, page=2, page_size=1, nopager=False)
        assert result == [2]

    def test_page_size_larger_than_list(self):
        items = [1, 2, 3]
        result = paginate_list(items, page=1, page_size=10, nopager=False)
        assert result == [1, 2, 3]

    def test_nopager_with_empty_list(self):
        result = paginate_list([], page=1, page_size=10, nopager=True)
        assert result == []
