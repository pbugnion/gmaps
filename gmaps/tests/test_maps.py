
import unittest

import traitlets

from .. import maps


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
