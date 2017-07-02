
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
        a = self.A(initial_viewport=maps.InitialViewport.from_zoom_center(3, (20.0, -5.0)))
        assert a.initial_viewport.zoom == 3
        assert a.initial_viewport.center == (20.0, -5.0)
