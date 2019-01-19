import unittest

import traitlets

from .. import errors_box


class ErrorsBox(unittest.TestCase):

    def test_no_errors(self):
        box = errors_box.ErrorsBox()
        assert box.get_state()["errors"] == []

    def test_with_errors(self):
        errors = ["first", "second"]
        box = errors_box.ErrorsBox(errors=errors)
        assert box.get_state()["errors"] == errors

    def test_change_errors(self):
        box = errors_box.ErrorsBox(errors=["first", "second"])
        new_errors = ["third"]
        box.errors = new_errors
        assert box.get_state()["errors"] == new_errors

    def test_refuse_non_unicode(self):
        with self.assertRaises(traitlets.TraitError):
            errors_box.ErrorsBox(errors=[42])
