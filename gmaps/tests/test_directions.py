
import unittest
import pytest

import traitlets

from ..directions import directions_layer


class DirectionsLayer(unittest.TestCase):

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

    def _add_default_options(self, **options):
        new_options = self.kwargs.copy()
        new_options.update(options)
        return new_options

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
