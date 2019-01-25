
import unittest

from .. import geojson_layer, InvalidGeoJson, GeoJsonFeature


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


class TestGeoJsonFeature(unittest.TestCase):

    def test_defaults(self):
        valid_feature_dict = {
            "type": "Feature",
            "geometry": {
                "type": "polygon",
                "coordinates": [[
                    [71.049, 38.408],
                    [71.334, 38.280]
                ]],
            },
            "properties": {"name": "Afghanistan"}
        }
        feature = GeoJsonFeature(feature=valid_feature_dict)
        state = feature.get_state()
        assert state["fill_opacity"] == 0.4
        assert state["stroke_opacity"] == 0.6
