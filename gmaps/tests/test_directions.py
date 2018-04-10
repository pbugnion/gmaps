
import unittest
import pytest

import traitlets

from ..directions import directions_layer, Directions


class DirectionsLayer(unittest.TestCase):

    def setUp(self):
        self.start = (51.0, 1.0)
        self.end = (50.0, 2.0)
        self.waypoints = [(52.0, 1.0), (52.0, 0.0)]
        self.data_array = [self.start] + self.waypoints + [self.end]

    def test_defaults(self):
        layer = Directions(start=self.start, end=self.end)
        state = layer.get_state()
        assert state['start'] == self.start
        assert state['end'] == self.end
        assert state['waypoints'] == []
        assert not state['avoid_ferries']
        assert not state['avoid_highways']
        assert not state['avoid_tolls']
        assert not state['optimize_waypoints']

    def test_pass_args(self):
        layer = Directions(self.start, self.end)
        state = layer.get_state()
        assert state['start'] == self.start
        assert state['end'] == self.end
        assert state['waypoints'] == []

    def test_set_data(self):
        layer = Directions(data=self.data_array)
        assert layer.start == self.start
        assert layer.end == self.end
        assert layer.waypoints == self.waypoints

    def test_change_data(self):
        layer = Directions(start=(0.0, 0.0), end=(2.0, 2.0))
        layer.data = self.data_array
        assert layer.start == self.start
        assert layer.end == self.end
        assert layer.waypoints == self.waypoints

    def test_waypoints_pandas_df(self):
        pd = pytest.importorskip("pandas")
        waypoints = pd.DataFrame.from_records(
            self.waypoints, columns=["latitude", "longitude"])
        layer = Directions(self.start, self.end, waypoints=waypoints)
        assert layer.waypoints == self.waypoints

    def test_allow_waypoints_none(self):
        layer = Directions(self.start, self.end, waypoints=None)
        assert layer.get_state()['waypoints'] == []

    def test_boolean_options(self):
        layer = Directions(
            self.start, self.end,
            avoid_ferries=True,
            avoid_highways=True,
            avoid_tolls=True,
            optimize_waypoints=True
        )
        state = layer.get_state()
        assert state['avoid_ferries']
        assert state['avoid_highways']
        assert state['avoid_tolls']
        assert state['optimize_waypoints']


class DirectionsFactory(unittest.TestCase):

    def setUp(self):
        self.start = (51.0, 1.0)
        self.end = (50.0, 2.0)
        self.waypoints = [(52.0, 1.0), (52.0, 0.0)]
        self.data_array_no_waypoints = [self.start, self.end]
        self.data_array = [self.start] + self.waypoints + [self.end]
        self.kwargs = {
            "avoid_ferries": False,
            "avoid_highways": False,
            "avoid_tolls": False,
            "optimize_waypoints": False
        }

    def test_no_waypoints(self):
        layer = directions_layer(self.start, self.end)
        assert layer.data == self.data_array_no_waypoints

    def test_waypoints(self):
        layer = directions_layer(self.start, self.end, self.waypoints)
        assert layer.data == self.data_array

    def test_no_waypoints_numpy_array(self):
        import numpy as np
        layer = directions_layer(np.array(self.start), self.end)
        assert layer.data == self.data_array_no_waypoints

    def test_waypoints_numpy_array(self):
        import numpy as np
        layer = directions_layer(
                np.array(self.start),
                self.end,
                np.array(self.waypoints)
        )
        assert layer.data == self.data_array

    def test_pandas_df(self):
        pd = pytest.importorskip("pandas")
        waypoints = pd.DataFrame.from_records(
            self.waypoints, columns=["latitude", "longitude"])
        layer = directions_layer(self.start, self.end, waypoints)
        assert layer.data == self.data_array

    def test_boolean_options(self):
        layer = directions_layer(
            self.start, self.end, waypoints=None,
            avoid_ferries=True,
            avoid_highways=True,
            avoid_tolls=True,
            optimize_waypoints=True
        )
        assert layer.avoid_ferries
        assert layer.avoid_highways
        assert layer.avoid_tolls
        assert layer.optimize_waypoints

    def test_travel_mode(self):
        layer = directions_layer(self.start, self.end, travel_mode='BICYCLING')
        assert layer.travel_mode == 'BICYCLING'

    def test_invalid_travel_mode(self):
        with self.assertRaises(traitlets.TraitError):
            directions_layer(self.start, self.end, travel_mode='wrong')
