
import unittest

import numpy as np

from ..bounds import (
    latitude_bounds, longitude_bounds, merge_longitude_bounds,
    MAX_ALLOWED_LATITUDE, MIN_ALLOWED_LATITUDE, EPSILON
)


class LatitudeBounds(unittest.TestCase):

    def test_latitude_bounds_single(self):
        latitudes = [-81.6297]
        lower, upper = latitude_bounds(latitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99 * EPSILON < diff < 2.01*EPSILON
        assert lower < -81.6297 < upper

    def test_latitude_bounds(self):
        latitudes = [10.0, 15.0, 20.0]
        lower, upper = latitude_bounds(latitudes)
        assert 5.0 < lower < 15.0
        assert 15.0 < upper < 25.0

    def test_latitude_whole_earth(self):
        latitudes = np.linspace(-89.0, 89.0, 100)
        lower, upper = latitude_bounds(latitudes)
        assert lower == MIN_ALLOWED_LATITUDE
        assert upper == MAX_ALLOWED_LATITUDE

    def test_extrema(self):
        latitudes = [89.0, -89.0]
        lower, upper = latitude_bounds(latitudes)
        assert lower == MIN_ALLOWED_LATITUDE
        assert upper == MAX_ALLOWED_LATITUDE

    def test_same_latitudes(self):
        latitudes = [-71.123, -71.123]
        lower, upper = latitude_bounds(latitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99*EPSILON < diff < 2.01*EPSILON
        assert lower < -71.123 < upper

    def test_similar_latitudes(self):
        latitudes = [-71.123, -71.123 + 0.01*EPSILON]
        lower, upper = latitude_bounds(latitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99*EPSILON < diff < 2.01*EPSILON
        assert lower < -71.123 < upper

    def test_latitude_single_extreme_low(self):
        latitudes = [-87.0]
        lower, upper = latitude_bounds(latitudes)
        assert upper > lower
        assert lower == MIN_ALLOWED_LATITUDE
        assert 0.9*EPSILON < upper - lower < 1.1*EPSILON

    def test_latitude_single_extreme_high(self):
        latitudes = [87.0]
        lower, upper = latitude_bounds(latitudes)
        assert upper > lower
        assert upper == MAX_ALLOWED_LATITUDE
        assert 0.9*EPSILON < upper - lower < 1.1*EPSILON


class LongitudeBounds(unittest.TestCase):

    def test_longitude_bounds_single(self):
        longitudes = [-87.6297]
        lower, upper = longitude_bounds(longitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99*EPSILON < diff < 2.01*EPSILON
        assert lower < -87.6297 < upper

    def test_longitude_bounds(self):
        longitudes = [10.0, 15.0, 20.0]
        lower, upper = longitude_bounds(longitudes)
        assert 5.0 < lower < 15.0
        assert 15.0 < upper < 25.0

    def test_negative_longitudes(self):
        longitudes = [-10.0, -15.0, -20.0]
        lower, upper = longitude_bounds(longitudes)
        assert -25.0 < lower < -15.0
        assert -15.0 < upper < -5.0

    def test_longitudes_whole_earth(self):
        longitudes = np.linspace(-179.0, 179.0, 100)
        lower, upper = longitude_bounds(longitudes)
        # either of these conditions result in google maps
        # showing entire planet
        assert (upper - lower > 180.0) or (upper < lower)

    def test_longitudes_around_dateline(self):
        longitudes = [179.0, -179.0]
        lower, upper = longitude_bounds(longitudes)
        print(lower, upper)
        assert 177.0 < lower < 180.0
        assert -180.0 < upper < -177.0

    def test_same_longitudes(self):
        longitudes = [-81.123, -81.123]
        lower, upper = longitude_bounds(longitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99*EPSILON < diff < 2.01*EPSILON
        assert lower < -81.123 < upper

    def test_similar_longitudes(self):
        longitudes = [-81.123, -81.123 + 0.01*EPSILON]
        lower, upper = longitude_bounds(longitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99*EPSILON < diff < 2.01*EPSILON
        assert lower < -81.123 < upper

    def test_same_longitudes_up_to_full_circle_rotation(self):
        longitudes = [10.0, 370.0]
        lower, upper = longitude_bounds(longitudes)
        assert upper > lower
        diff = abs(upper - lower)
        assert 1.99*EPSILON < diff < 2.01*EPSILON
        assert lower < 10.0 < upper


class MergeLongitudeBounds(unittest.TestCase):

    def _verify_bounds(self, bounds, expected_lower, expected_upper):
        lower, upper = merge_longitude_bounds(bounds)
        assert lower == expected_lower
        assert upper == expected_upper

    def test_merge_longitude_bounds(self):
        bounds = [(10.0, 20.0), (15.0, 25.0)]
        self._verify_bounds(bounds, 10.0, 25.0)

    def test_merge_overlapping_bounds(self):
        bounds = [(5.0, 55.0), (20.0, 25.0)]
        self._verify_bounds(bounds, 5.0, 55.0)

    def test_merge_negative_bounds(self):
        bounds = [(-25.0, 5.0), (10.0, 15.0)]
        self._verify_bounds(bounds, -25.0, 15.0)

    def test_merge_whole_earth(self):
        whole_earth_longitudes = np.linspace(-179.0, 179.0, 100)
        whole_earth_bounds = longitude_bounds(whole_earth_longitudes)
        bounds = [whole_earth_bounds, (10.0, 15.0)]
        self._verify_bounds(bounds, *whole_earth_bounds)

    def test_single_bounds(self):
        bounds = (10.0, 20.0)
        self._verify_bounds([bounds], *bounds)

    def test_verify_no_bounds(self):
        self._verify_bounds([], -180.0, -180.0)
