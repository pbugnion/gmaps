
import unittest

from .. import geojson_layer, InvalidGeoJson


class GeoJson(unittest.TestCase):

    def test_raise_on_empty_geometry(self):
        geo = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": None,
                    "properties": {"a": 5}
                }
            ]
        }
        with self.assertRaises(InvalidGeoJson):
            geojson_layer(geo)

    def test_raises_on_empty_geojson(self):
        geo = {}
        with self.assertRaises(InvalidGeoJson):
            geojson_layer(geo)

    def test_raises_not_feature_collection(self):
        geo = {
            "type": "Feature",
            "geometry": None,
            "properties": {"a": 5}
        }
        with self.assertRaises(InvalidGeoJson):
            geojson_layer(geo)
