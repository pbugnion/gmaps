
import unittest

import gmaps


class TestHeatmapOptionsMixin(unittest.TestCase):

    def test_gradient_default_none(self):
        l = gmaps.maps._HeatmapOptionsMixin()
        assert l.gradient is None

    def test_gradient_default_values(self):
        l = gmaps.maps._HeatmapOptionsMixin(gradient=["blue", "red"])
        assert l.gradient == ["blue", "red"]

    def test_gradient_set_none(self):
        l = gmaps.maps._HeatmapOptionsMixin(gradient=["blue", "red"])
        l.gradient = None
        assert l.gradient is None
