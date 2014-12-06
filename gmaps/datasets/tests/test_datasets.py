
import unittest

import gmaps.datasets as datasets

class TestDatasets(unittest.TestCase):

	def test_list_datasets(self):
		assert 'taxi_rides' in datasets.list_datasets()

	def test_load_datasets(sefl):
		data = datasets.load_dataset('taxi_rides')
		assert data.shape == (500,)
		assert data.dtype.names == ('Latitude', 'Longitude')