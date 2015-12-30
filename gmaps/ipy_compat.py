
# Provides a compatibility layer between different versions of IPython

import IPython
ipy_version = IPython.version_info[0]

# conditional import of the widgets module
if ipy_version in (2, 3):
    from IPython.html import widgets
else:
    # IPython 4
    from ipywidgets import widgets

import _traitlets as traitlets

def FloatOrNone(**kwargs):
    """
    Emulate Float(allow_none=True) in IPython 2.3.
    """
    if ipy_version == 2:
        return traitlets.Instance(float, allow_none=True, **kwargs)
    else:
        return traitlets.CFloat(allow_none=True, default_value=None, **kwargs)
