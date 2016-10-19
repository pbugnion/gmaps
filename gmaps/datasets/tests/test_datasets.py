
import unittest

import pytest

from .. import datasets


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

    def test_dataset_metadata(self):
        meta = datasets.dataset_metadata('taxi_rides')
        assert 'description' in meta
        assert 'headers' in meta
        assert 'url' not in meta

    def test_load_as_df_taxi_rides(self):
        pytest.importorskip("pandas")  # only run this if pandas is available
        df = datasets.load_dataset_as_df('taxi_rides')
        assert df.columns.tolist() == ['latitude', 'longitude']
        assert df.dtypes.tolist() == [float, float]
