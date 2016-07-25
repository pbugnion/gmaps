
import sys

import traitlets

class NullableList(traitlets.List):

    def __init__(self, trait=None, default_value=None, minlen=0, maxlen=sys.maxsize, **metadata):
        super(NullableList, self).__init__(
            trait=trait,
            default_value=default_value,
            minlen=minlen, maxlen=maxlen, **metadata)

        self.allow_none = True
        if default_value is None:
            self.default_value = None
