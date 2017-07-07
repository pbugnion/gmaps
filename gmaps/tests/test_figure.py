import unittest

from ..figure import figure


class TestFigureFactory(unittest.TestCase):

    def test_defaults(self):
        fig = figure()
        assert fig._toolbar is not None
        assert fig._errors_box is not None
        map_ = fig._map
        assert map_ is not None
        assert map_.initial_viewport == "DATA_BOUNDS"

    def test_zoom_center(self):
        center = (10.0, 20.0)
        fig = figure(zoom_level=10, center=center)
        map_ = fig._map
        assert map_.initial_viewport.zoom_level == 10
        assert map_.initial_viewport.center == center

    def test_zoom_no_center(self):
        with self.assertRaises(ValueError):
            figure(zoom_level=10)

    def test_center_no_zoom(self):
        with self.assertRaises(ValueError):
            figure(center=(10.0, 20.0))
