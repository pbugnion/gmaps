
import unittest

from .. import geojson_geometries


class TestGeoJsonGeometries(unittest.TestCase):

    def test_list_datasets(self):
        assert 'countries' in geojson_geometries.list_geometries()
