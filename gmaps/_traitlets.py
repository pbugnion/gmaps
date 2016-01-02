
# The 'traitlets' module is in a different location in IPython 3 vs. Jupyter.
# This interface is designed to sit  in front of 'traitlets'
# and hide its location.
# Always import this module, rather than traitlets directly:
#
# import _traitlets as traitlets
#
# See, eg. 'http://jupyter.readthedocs.org/en/latest/migrating.html#imports'.

from .ipy_compat import ipy_version

if ipy_version == 3:
    from IPython.utils.traitlets import *
else:
    # IPython 4
    from traitlets import *
