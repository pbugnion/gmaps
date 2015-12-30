
import gmaps._traitlets as traitlets
import gmaps.utils as utils

from ipy_compat import ipy_version

class CSSDimension(traitlets.TraitType):

    default_value = u'0'
    info_text = u'A CSS dimension'

    def validate(self, obj, value):
        value = utils.parse_css_dimension(value)
        return value


def FloatOrNone(**kwargs):
    """
    Emulate Float(allow_none=True) in IPython 2.3.
    """
    if ipy_version == 2:
        return traitlets.Instance(float, allow_none=True, **kwargs)
    else:
        return traitlets.CFloat(allow_none=True, default_value=None, **kwargs)
