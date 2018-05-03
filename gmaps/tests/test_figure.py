import unittest

from ..figure import figure, Figure, FigureLayout
from ..maps import Map


class TestFigure(unittest.TestCase):

    def test_proxy_map_type(self):
        fig = Figure(_map=Map(), map_type='HYBRID')
        assert fig.map_type == 'HYBRID'
        assert fig._map.map_type == 'HYBRID'

    def test_proxy_map_type_change(self):
        fig = Figure(_map=Map(), map_type='HYBRID')
        fig.map_type = 'TERRAIN'
        assert fig._map.map_type == 'TERRAIN'

    def test_catch_map_type_change_in_map(self):
        fig = Figure(_map=Map(), map_type='HYBRID')
        fig._map.map_type = 'TERRAIN'
        assert fig.map_type == 'TERRAIN'

    def test_proxy_mouse_handling(self):
        fig = Figure(_map=Map(), mouse_handling='GREEDY')
        assert fig.mouse_handling == 'GREEDY'
        assert fig._map.mouse_handling == 'GREEDY'

    def test_proxy_mouse_handling_change(self):
        fig = Figure(_map=Map(), mouse_handling='GREEDY')
        fig.mouse_handling = 'NONE'
        assert fig._map.mouse_handling == 'NONE'

    def test_catch_mouse_handling_change_in_map(self):
        fig = Figure(_map=Map(), mouse_handling='GREEDY')
        fig._map.mouse_handling = 'NONE'
        assert fig.mouse_handling == 'NONE'


class TestFigureFactory(unittest.TestCase):

    def test_defaults(self):
        fig = figure()
        assert fig._toolbar is not None
        assert fig._errors_box is not None
        assert fig.map_type == 'ROADMAP'
        assert fig.mouse_handling == 'COOPERATIVE'
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

    def test_custom_map_type(self):
        fig = figure(map_type='SATELLITE')
        assert fig.map_type == 'SATELLITE'

    def test_0_tilt(self):
        fig = figure(tilt=0)
        assert fig._map.tilt == 0

    def test_45_tilt(self):
        fig = figure(tilt=45)
        assert fig._map.tilt == 45

    def test_default_tilt(self):
        fig = figure()
        assert fig._map.tilt == 45

    def test_custom_mouse_handling(self):
        fig = figure(mouse_handling='NONE')
        assert fig.mouse_handling == 'NONE'
