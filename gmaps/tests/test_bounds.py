
import unittest
import pytest

import numpy as np

from ..bounds import latitude_bounds, longitude_bounds

class LatitudeBounds(unittest.TestCase):

    def test_latitude_bounds(self):
        latitudes = [10.0, 15.0, 20.0]
        lower, upper = latitude_bounds(latitudes)
        assert 5.0 < lower < 15.0
        assert 15.0 < upper < 25.0

    def test_latitude_whole_earth(self):
        latitudes = np.linspace(-89.0, 89.0, 100)
        lower, upper = latitude_bounds(latitudes)
        assert -90.0 < lower < -89.0
        assert 89.0 < upper < 90.0

    def test_extrema(self):
        latitudes = [89.0, -89.0]
        lower, upper = latitude_bounds(latitudes)
        print(lower, upper)
        assert -90.0 < lower < -87.0
        assert 87.0 < upper < 90.0

