
import unittest

import traitlets

import gmaps.geotraitlets as geotraitlets


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

    def test_allow_none(self):
        class A(traitlets.HasTraits):
            x = geotraitlets.ColorAlpha(default_value=None, allow_none=True)
        a = A()
        assert a.x is None
        a = A(x="blue")
        assert a.x == "blue"
