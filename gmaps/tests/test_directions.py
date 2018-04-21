
import unittest
import pytest

import traitlets

from ..directions import Directions, DEFAULT_STROKE_COLOR


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
        assert state['show_markers']
        assert state['show_route']
        assert state['stroke_color'].lower() == DEFAULT_STROKE_COLOR.lower()
        assert state['stroke_opacity'] == 0.6
        assert state['stroke_weight'] == 6.0

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

    def test_no_waypoints_numpy_array(self):
        import numpy as np
        layer = Directions(np.array(self.start), np.array(self.end))
        state = layer.get_state()
        assert state['start'] == self.start
        assert state['end'] == self.end

    def test_waypoints_numpy_array(self):
        import numpy as np
        layer = Directions(
                np.array(self.start),
                self.end,
                np.array(self.waypoints)
        )
        state = layer.get_state()
        assert state['start'] == self.start
        assert state['end'] == self.end
        assert state['waypoints'] == self.waypoints

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

    def test_show_markers_routes(self):
        layer = Directions(
            self.start, self.end,
            show_markers=False,
            show_route=False
        )
        state = layer.get_state()
        assert not state['show_markers']
        assert not state['show_route']

    def test_change_markers_routes(self):
        layer = Directions(self.start, self.end)
        layer.show_markers = False
        assert not layer.get_state()['show_markers']
        layer.show_route = False
        assert not layer.get_state()['show_route']

    def test_travel_mode(self):
        layer = Directions(self.start, self.end, travel_mode='BICYCLING')
        assert layer.travel_mode == 'BICYCLING'

    def test_invalid_travel_mode(self):
        with self.assertRaises(traitlets.TraitError):
            Directions(self.start, self.end, travel_mode='wrong')

    def test_stroke_options(self):
        layer = Directions(
            self.start, self.end,
            stroke_color=(10, 20, 30),
            stroke_opacity=0.2,
            stroke_weight=20
        )
        state = layer.get_state()
        assert state['stroke_color'] == 'rgb(10,20,30)'
        assert state['stroke_opacity'] == 0.2
        assert state['stroke_weight'] == 20

    def test_change_stroke_options(self):
        layer = Directions(self.start, self.end)
        layer.stroke_color = (10, 20, 30)
        assert layer.get_state()['stroke_color'] == 'rgb(10,20,30)'
        layer.stroke_opacity = 0.2
        assert layer.get_state()['stroke_opacity'] == 0.2
        layer.stroke_weight = 20
        assert layer.get_state()['stroke_weight'] == 20

    def test_invalid_opacity(self):
        with self.assertRaises(traitlets.TraitError):
            Directions(self.start, self.end, stroke_opacity=20.0)
