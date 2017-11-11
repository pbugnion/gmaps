from ._version import __version__  # noqa

from .figure import *  # noqa
from .maps import *  # noqa
from .marker import *  # noqa
from .heatmap import *  # noqa
from .directions import *  # noqa
from .geojson_layer import *  # noqa
from .bicycling import *  # noqa
from .transit import *  # noqa
from .traffic import *  # noqa
from .drawing import *  # noqa


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-gmaps',
        'require': 'jupyter-gmaps/extension'
    }]
