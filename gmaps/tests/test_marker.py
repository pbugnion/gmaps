
import unittest

from ..marker import _marker_layer_options


class MarkerLayer(unittest.TestCase):

    def setUp(self):
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]

    def test_hover_text_atomic(self):
        marker_options = _marker_layer_options(
            self.locations, hover_text="test-text", label="")
        for options in marker_options:
            assert options["hover_text"] == "test-text"

    def test_hover_text_lists(self):
        marker_options = _marker_layer_options(
            self.locations, hover_text=["t1", "t2"], label="")
        assert tuple(options["hover_text"] for options in marker_options) == ("t1", "t2")
