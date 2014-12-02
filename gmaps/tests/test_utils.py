

import unittest

import gmaps.utils as utils

class Test_ParseCssDimension(unittest.TestCase):

    def test_int(self):
        assert utils.parse_css_dimension(700) == "700px"
        assert utils.parse_css_dimension(20) == "20px"

    def test_str_no_units(self):
        assert utils.parse_css_dimension("700") == "700px"
        assert utils.parse_css_dimension("20") == "20px"

    def test_str_with_units(self):
        assert utils.parse_css_dimension("70em") == "70em"
        assert utils.parse_css_dimension("200px") == "200px"

    def test_str_with_whitespace(self):
        assert utils.parse_css_dimension("70em ") == "70em"
        assert utils.parse_css_dimension(" 70 ") == "70px"

    def test_str_internal_whitespace(self):
        assert utils.parse_css_dimension("200 px") == "200px"
        assert utils.parse_css_dimension("200 em") == "200em"



