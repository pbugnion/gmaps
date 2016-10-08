
import unittest

import gmaps.datasets as datasets


class TestDatasets(unittest.TestCase):

    def test_list_datasets(self):
        assert 'taxi_rides' in datasets.list_datasets()

    def test_load_datasets(self):
        data = datasets.load_dataset('taxi_rides')
        assert data[0] == (37.782551, -122.445368)
        assert len(data) == 500

    def test_load_datasets_magnitude(self):
        data = datasets.load_dataset('earthquakes')
        assert data[0] == (65.1933, -149.0725, 1.7)
        assert len(data) == 8604
