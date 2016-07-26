
import sys

import traitlets

class NullableList(traitlets.List):
    """
    Traitlet for an attribute that can either be a list or None

    This is different from List() inasmuch as List(default_value=None)
    defaults to an empty list, whereas NullableList(default_value=None)
    defaults to None.
    """

    def __init__(self, trait=None, default_value=None, minlen=0, maxlen=sys.maxsize, **metadata):
        super(NullableList, self).__init__(
            trait=trait,
            default_value=default_value,
            minlen=minlen, maxlen=maxlen, **metadata)

        self.allow_none = True
        if default_value is None:
            self.default_value = None
