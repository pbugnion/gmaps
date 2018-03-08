import unittest

from ..figure import figure, FigureLayout


class TestFigureFactory(unittest.TestCase):

    def test_defaults(self):
        fig = figure()
        assert fig._toolbar is not None
        assert fig._errors_box is not None
        map_ = fig._map
        assert map_ is not None
        assert map_.initial_viewport == 'DATA_BOUNDS'

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

    def test_set_map_layout(self):
        fig = figure()
        map_ = fig._map
        assert map_.layout.width == '100%'
        assert map_.layout.height == '100%'

    def test_default_layout(self):
        fig = figure()
        assert fig.layout.height == '420px'

    def test_custom_layout(self):
        layout = FigureLayout(
            height='350px', width='712px', border='1px solid blue')
        fig = figure(layout=layout)
        assert fig.layout.height == layout.height
        assert fig.layout.width == layout.width
        assert fig.layout.border == layout.border

    def test_custom_layout_default_height(self):
        layout = FigureLayout(
            width='712px', border='1px solid blue')
        fig = figure(layout=layout)
        assert fig.layout.height == '420px'

    def test_custom_layout_as_dict(self):
        layout = dict(
            height='350px', width='712px', border='1px solid blue')
        fig = figure(layout=layout)
        assert fig.layout.height == layout['height']
        assert fig.layout.width == layout['width']
        assert fig.layout.border == layout['border']
