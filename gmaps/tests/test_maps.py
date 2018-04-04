
import unittest

import traitlets

from .. import maps, heatmap_layer


class Map(unittest.TestCase):

    def test_defaults(self):
        m = maps.Map()
        state = m.get_state()
        assert state['map_type'] == 'ROADMAP'
        assert state['mouse_handling'] == 'COOPERATIVE'
        assert state['initial_viewport'] == {'type': 'DATA_BOUNDS'}
        assert state['layers'] == []

    def test_custom_traits(self):
        test_layer = heatmap_layer([(1.0, 2.0), (3.0, 4.0)])
        m = maps.Map(
            map_type='HYBRID',
            mouse_handling='NONE',
            initial_viewport=maps.InitialViewport.from_zoom_center(
                10, (5.0, 10.0)),
            layers=[test_layer]
        )
        state = m.get_state()
        assert state['map_type'] == 'HYBRID'
        assert state['initial_viewport'] == {
            'type': 'ZOOM_CENTER',
            'center': (5.0, 10.0),
            'zoom_level': 10
        }
        assert state['layers'] == ['IPY_MODEL_' + test_layer.model_id]
        assert state['mouse_handling'] == 'NONE'


class InitialViewport(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            initial_viewport = maps.InitialViewport()
        self.A = A

    def test_accept_data_bounds(self):
        a = self.A(initial_viewport=maps.InitialViewport.from_data_bounds())
        assert a.initial_viewport == "DATA_BOUNDS"

    def test_accept_zoom_center(self):
        viewport = maps.InitialViewport.from_zoom_center(3, (20.0, -5.0))
        a = self.A(initial_viewport=viewport)
        assert a.initial_viewport.zoom_level == 3
        assert a.initial_viewport.center == (20.0, -5.0)


class SerializeViewport(unittest.TestCase):

    def test_serialize_databounds(self):
        viewport = maps.InitialViewport.from_data_bounds()
        expected = {'type': 'DATA_BOUNDS'}
        assert maps._serialize_viewport(viewport, None) == expected

    def test_serialize_zoom_center(self):
        viewport = maps.InitialViewport.from_zoom_center(3, (20.0, -5.0))
        expected = {
            'type': 'ZOOM_CENTER',
            'center': (20.0, -5.0),
            'zoom_level': 3
        }
        assert maps._serialize_viewport(viewport, None) == expected
