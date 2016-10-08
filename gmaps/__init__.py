from ._version import version_info, __version__  # noqa

from .maps import *  # noqa
from .marker import *  # noqa


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-gmaps',
        'require': 'jupyter-gmaps/extension'
    }]
