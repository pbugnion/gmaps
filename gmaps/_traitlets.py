
from ipy_compat import ipy_version

if ipy_version in (2, 3):
    from IPython.utils.traitlets import *
else:
    # IPython 4
    from traitlets import *
