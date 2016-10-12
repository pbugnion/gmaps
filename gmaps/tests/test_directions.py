
import unittest
import pytest

from ..directions import _directions_options


class DirectionsLayer(unittest.TestCase):

    def setUp(self):
        self.start = (51.0, 1.0)
        self.end = (50.0, 2.0)
        self.waypoints = [(52.0, 1.0), (52.0, 0.0)]
        self.data_array_no_waypoints = [self.start, self.end]
        self.data_array = [self.start] + self.waypoints + [self.end]

    def test_no_waypoints(self):
        options = _directions_options(
            self.start, self.end, waypoints=None)["data"]
        assert options == self.data_array_no_waypoints

    def test_waypoints(self):
        options = _directions_options(
            self.start, self.end, self.waypoints)["data"]
        assert options == self.data_array

    def test_no_waypoints_numpy_array(self):
        import numpy as np
        options = _directions_options(
            np.array(self.start), self.end, None)["data"]
        assert options == self.data_array_no_waypoints

    def test_waypoints_numpy_array(self):
        import numpy as np
        options = _directions_options(
            np.array(self.start), self.end, np.array(self.waypoints))["data"]
        assert options == self.data_array

    def test_pandas_df(self):
        pd = pytest.importorskip("pandas")
        waypoints = pd.DataFrame.from_records(
            self.waypoints, columns=["latitude", "longitude"])
        options = _directions_options(
            self.start, self.end, waypoints)["data"]
        assert options == self.data_array
