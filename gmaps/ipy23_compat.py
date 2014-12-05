
import IPython
from IPython.utils.traitlets import Instance, CFloat

IPy23 = (IPython.version_info[0] == 2) # true if IPython version is 2.3.

def FloatOrNone(**kwargs):
    """
    Emulate Float(allow_none=True) in IPython 2.3.
    """
    if IPy23:
        return Instance(float, allow_none=True, **kwargs)
    else:
        return CFloat(allow_none=True, default_value=None, **kwargs)

