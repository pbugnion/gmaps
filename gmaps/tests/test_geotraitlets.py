
import unittest
import pytest

import traitlets

from .. import geotraitlets


class LocationArray(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.LocationArray()
        self.A = A
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]

    def test_accept_list(self):
        a = self.A(x=self.locations)
        assert a.x == self.locations

    def test_accept_np_array(self):
        import numpy as np
        a = self.A(x=np.array(self.locations))
        assert a.x == self.locations

    def test_accept_dataframe(self):
        pd = pytest.importorskip('pandas')
        df = pd.DataFrame.from_records(
            self.locations, columns=['latitude', 'longitude'])
        a = self.A(x=df)
        assert a.x == self.locations

    def test_reject_invalid_latitude(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=[('not-a', 'latitude')])

    def test_reject_outofbounds_latitude(self):
        with self.assertRaises(geotraitlets.InvalidPointException):
            self.A(x=[(-100.0, 0.0)])

    def test_reject_outofbounds_longitude(self):
        with self.assertRaises(geotraitlets.InvalidPointException):
            self.A(x=[(0.0, 200.0)])

    def test_minlen(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.LocationArray(minlen=2)
        A(x=self.locations)
        with self.assertRaises(traitlets.TraitError):
            A(x=[])

    def test_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.LocationArray(allow_none=True)
        a = A(x=None)
        assert a.x is None

    def test_dont_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.LocationArray(allow_none=False)
        with self.assertRaises(traitlets.TraitError):
            A(x=None)


class WeightArray(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.WeightArray()
        self.A = A
        self.weights = [1.0, 3.5]

    def test_accept_list(self):
        a = self.A(x=self.weights)
        assert a.x == self.weights

    def test_accept_np_array(self):
        import numpy as np
        a = self.A(x=np.array(self.weights))
        assert a.x == self.weights

    def test_accept_series(self):
        pd = pytest.importorskip('pandas')
        a = self.A(x=pd.Series(self.weights))
        assert a.x == self.weights

    def test_reject_negative_weight(self):
        with self.assertRaises(geotraitlets.InvalidWeightException):
            self.A(x=[-2.0])

    def test_minlen(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.WeightArray(minlen=2)
        a = A(x=self.weights)
        assert a.x == self.weights
        with self.assertRaises(traitlets.TraitError):
            A(x=[1.0])

    def test_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.WeightArray(allow_none=True)
        a = A(x=None)
        assert a.x is None

    def test_dont_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.WeightArray(allow_none=False)
        a = A(x=self.weights)
        assert a.x == self.weights
        with self.assertRaises(traitlets.TraitError):
            a.x = None


class ColorString(unittest.TestCase):
    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ColorString()
        self.A = A

    def test_accept_simple_color(self):
        a = self.A(x='blue')
        assert a.x == 'blue'

    def test_reject_misspelled_color(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x='gren')

    def test_accept_hex_triple(self):
        a = self.A(x='#aabbcc')
        assert a.x == '#aabbcc'

    def test_accept_hex_short_triple(self):
        a = self.A(x='#abc')
        assert a.x == '#abc'

    def test_accept_rgb_string(self):
        a = self.A(x='rgb(100, 0, 0)')
        assert a.x == 'rgb(100,0,0)'

    def test_accept_rgba_string(self):
        a = self.A(x='rgba(100, 0, 0,0.5)')
        assert a.x == 'rgba(100,0,0,0.5)'

    def test_accept_rgba_string_alpha_one(self):
        a = self.A(x='rgba(100, 0, 0, 1.0)')
        assert a.x == 'rgba(100,0,0,1.0)'

    def test_accept_rgba_string_alpha_one_int(self):
        a = self.A(x='rgba(100, 0, 0, 1)')
        assert a.x == 'rgba(100,0,0,1)'

    def test_accept_rgba_string_alpha_zero_int(self):
        a = self.A(x='rgba(100, 0, 0, 0)')
        assert a.x == 'rgba(100,0,0,0)'

    def test_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ColorString(
                allow_none=True, default_value=None)
        a = A()
        assert a.x is None

    def test_allow_none_accept_string(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ColorString(
                allow_none=True, default_value=None)
        a = A(x='green')
        assert a.x == 'green'


class TestRgbTuple(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.RgbTuple()
        self.A = A

    def test_accepts_tuples(self):
        a = self.A(x=(100, 0, 250))
        assert a.x == (100, 0, 250)

    def test_reject_tuples_wrong_length(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=(100, 2))

    def test_reject_tuples_wrong_numbers(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=(300, 0, 0))
        with self.assertRaises(traitlets.TraitError):
            self.A(x=(200, -10, 0))

    def test_default_value(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.RgbTuple(default_value=(100, 0, 250))
        assert A().x == (100, 0, 250)


class TestRgbaTuple(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.RgbaTuple()
        self.A = A

    def test_accepts_tuples(self):
        a = self.A(x=(100, 0, 250, 0.5))
        assert a.x == (100, 0, 250, 0.5)

    def test_reject_tuples_wrong_numbers(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=(200, 0, 0, -0.5))

    def test_default_value(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.RgbaTuple(default_value=(100, 0, 250, 0.5))
        assert A().x == (100, 0, 250, 0.5)


class TestColorAlpha(unittest.TestCase):
    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ColorAlpha()
        self.A = A

    def test_accept_string(self):
        a = self.A(x="blue")
        assert a.x == "blue"

    def test_accept_rgb_tuple(self):
        a = self.A(x=(100, 0, 10))
        assert a.x == 'rgb(100,0,10)'

    def test_accept_rgba_tuple(self):
        a = self.A(x=(100, 0, 10, 0.5))
        assert a.x == 'rgba(100,0,10,0.5)'

    def test_accept_rgba_tuple_alpha_one(self):
        a = self.A(x=(100, 0, 250, 1.0))
        assert a.x == 'rgba(100,0,250,1.0)'

    def test_accept_rgba_tuple_alpha_one_int(self):
        a = self.A(x=(100, 0, 250, 1))
        assert a.x == 'rgba(100,0,250,1.0)'

    def test_accept_rgba_tuple_alpha_zero(self):
        a = self.A(x=(100, 0, 250, 0.0))
        assert a.x == 'rgba(100,0,250,0.0)'

    def test_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ColorAlpha(default_value=None, allow_none=True)
        a = A()
        assert a.x is None
        a = A(x="blue")
        assert a.x == "blue"


class TestZoomLevel(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ZoomLevel()
        self.A = A

    def test_accept_zoom(self):
        a = self.A(x=8)
        assert a.x == 8

    def test_reject_high_value(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=22)

    def test_reject_negative_value(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=-1)


class TestMapType(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.MapType('ROADMAP')
        self.A = A

    def test_default_value(self):
        a = self.A()
        assert a.x == 'ROADMAP'

    def test_accept_valid_values(self):
        for map_type in ['ROADMAP', 'HYBRID', 'SATELLITE', 'TERRAIN']:
            a = self.A(x=map_type)
            assert a.x == map_type

    def test_reject_invalid(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x='not-a-map-type')

    def test_reject_none(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=None)


class TestMouseHandling(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.MouseHandling('COOPERATIVE')
        self.A = A

    def test_default_value(self):
        a = self.A()
        assert a.x == 'COOPERATIVE'

    def test_accept_valid_values(self):
        for behaviour in ['COOPERATIVE', 'GREEDY', 'NONE', 'AUTO']:
            a = self.A(x=behaviour)
            assert a.x == behaviour

    def test_reject_invalid(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x='not-a-mouse-handling-behaviour')

    def test_reject_none(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=None)


class Point(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.Point()
        self.A = A

    def test_default_value(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.Point((1.0, 2.0))
        a = A()
        assert a.x == (1.0, 2.0)

    def test_tuple(self):
        a = self.A(x=(5.0, 10.0))
        assert a.x == (5.0, 10.0)

    def test_list(self):
        a = self.A(x=[5.0, 10.0])
        assert a.x == (5.0, 10.0)

    def test_nparray(self):
        import numpy as np
        a = self.A(x=np.array([5.0, 10.0]))
        assert a.x == (5.0, 10.0)


class TestOpacity(unittest.TestCase):

    def setUp(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.Opacity()
        self.A = A

    def test_default_value(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.Opacity(default_value=0.5)
        a = A()
        assert a.x == 0.5

    def test_set_value(self):
        a = self.A(x=0.3)
        assert a.x == 0.3

    def test_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.Opacity(allow_none=True, default_value=None)
        assert A().x is None
        assert A(x=0.1).x == 0.1

    def test_under_min(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=-1.0)

    def test_over_max(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x=2.0)

    def test_wrong_type(self):
        with self.assertRaises(traitlets.TraitError):
            self.A(x='not-a-float')
