from ._version import version_info, __version__

from .maps import *
from .marker import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-gmaps',
        'require': 'jupyter-gmaps/extension'
    }]
