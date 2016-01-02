
# The 'widgets' module is in a different location in IPython 3 vs. Jupyter.
# This interface is designed to sit  in front of 'ipywidget'
# and hide its location.
# Always import this module, rather than ipywidget directly:
#
# from _ipywidget import widgets
#
# See, eg. 'http://jupyter.readthedocs.org/en/latest/migrating.html#imports'.

from .ipy_compat import ipy_version

if ipy_version == 3:
    from IPython.html import widgets
else:
    # IPython 4
    from ipywidgets import widgets
