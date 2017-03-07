
import unittest

from .. import geojson_geometries


class TestGeoJsonGeometries(unittest.TestCase):

    def test_list_datasets(self):
        assert 'countries' in geojson_geometries.list_geometries()

    def test_load_geometries(self):
        geometry = geojson_geometries.load_geometry('countries')
        assert 'features' in geometry
        assert geometry['type'] == 'FeatureCollection'
