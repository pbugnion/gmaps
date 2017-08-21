
import unittest

from ..traffic import traffic_layer


class TrafficLayer(unittest.TestCase):

    def test_defaults(self):
        layer = traffic_layer()
        assert layer.get_state()['auto_refresh']

    def test_no_auto_refresh(self):
        layer = traffic_layer(auto_refresh=False)
        assert not layer.get_state()['auto_refresh']
