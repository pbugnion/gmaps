
import ipywidgets as widgets
from traitlets import (Unicode, default, List, Tuple, Instance,
                       observe, Dict, HasTraits, Enum, Union)

from .bounds import merge_longitude_bounds
from .geotraitlets import Point, ZoomLevel, MapType, MouseHandling, Tilt
from ._docutils import doc_subst
from ._version import CLIENT_VERSION

DEFAULT_CENTER = (46.2, 6.1)
DEFAULT_BOUNDS = [(46.2, 6.1), (47.2, 7.1)]

_default_configuration = {'api_key': None}


map_params_doc_snippets = {}

map_params_doc_snippets['map_type'] = """
    :param map_type:
        String representing the type of map to show. One of 'ROADMAP' (the
        classic Google Maps style) 'SATELLITE' (just satellite tiles with no
        overlay), 'HYBRID' (satellite base tiles but with features such as
        roads and cities overlaid) and 'TERRAIN' (map showing terrain
        features). Defaults to 'ROADMAP'.
    :type map_type: str, optional
"""

map_params_doc_snippets['mouse_handling'] = """
    :param mouse_handling:
        String representing how the map captures the page's mouse event. One of
        'COOPERATIVE' (scroll events scroll the page without zooming the map,
        double clicks or CTRL/CMD+scroll zoom the map), 'GREEDY' (the map
        captures all scroll events), 'NONE' (the map cannot be zoomed or panned
        by user gestures) or 'AUTO' (cooperative if the notebook is displayed
        in an iframe, greedy otherwise). Defaults to 'COOPERATIVE'.
    :type mouse_handling: str, optional
"""


def configure(api_key=None):
    """
    Configure access to the GoogleMaps API.

    :param api_key: String denoting the key to use when accessing Google maps,
        or None to not pass an API key.
    """
    configuration = {'api_key': api_key}
    global _default_configuration
    _default_configuration = configuration


class ConfigurationMixin(HasTraits):
    configuration = Dict(
        traits={'api_key': Unicode(allow_none=True)}).tag(sync=True)

    @default('configuration')
    def _configuration_default(self):
        return _default_configuration


class GMapsWidgetMixin(HasTraits):
    """
    Traitlets that are constant across all of gmaps
    """
    _model_module = Unicode('jupyter-gmaps').tag(sync=True)
    _view_module = Unicode('jupyter-gmaps').tag(sync=True)
    _model_module_version = Unicode(CLIENT_VERSION).tag(sync=True)
    _view_module_version = Unicode(CLIENT_VERSION).tag(sync=True)


class InitialViewport(Union):
    """
    Traitlet defining the initial viewport for a map.
    """
    def __init__(self, **metadata):
        trait_types = [
                Enum(['DATA_BOUNDS']),
                Instance(_ZoomCenter)
        ]
        super(InitialViewport, self).__init__(trait_types, **metadata)

    @staticmethod
    def from_data_bounds():
        """
        Create a viewport centered on the map's data.

        Most of the time, you should rely on the defaults provided by the
        :func:`gmaps.figure` factory method, rather than creating a
        viewport yourself.

        :Examples:

        >>> m = gmaps.Map(initial_viewport=InitialViewport.from_data_bounds())
        """
        return 'DATA_BOUNDS'

    @staticmethod
    def from_zoom_center(zoom_level, center):
        """
        Create a viewport by explicitly setting the zoom and center

        Most of the time, you should rely on the defaults provided by the
        :func:`gmaps.figure` factory method, rather than creating a
        viewport yourself.

        :param zoom_level:
            The zoom level for the map. A value between 0 (zoomed out) and
            21 (zoomed in). Note that the highest zoom levels are only
            available in some regions of the world (e.g. cities).
        :type zoom_level: int

        :param center:
            (Latitude, longitude) pair denoting the map center.
        :type center: tuple of floats

        :Examples:

        >>> zoom_level = 8
        >>> center = (20.0, -10.0)
        >>> viewport = InitialViewport.from_zoom_center(zoom_level, center)
        >>> m = gmaps.figure(initial_viewport=viewport)
        """
        return _ZoomCenter(zoom_level=zoom_level, center=center)


class _ZoomCenter(HasTraits):
    zoom_level = ZoomLevel(default_value=8)
    center = Point(default_value=DEFAULT_CENTER)


def _serialize_viewport(viewport, manager):
    if viewport == 'DATA_BOUNDS':
        payload = {'type': 'DATA_BOUNDS'}
    else:
        try:
            payload = {
                    'type': 'ZOOM_CENTER',
                    'center': viewport.center,
                    'zoom_level': viewport.zoom_level
            }
        except AttributeError:
            raise ValueError('viewport')
    return payload


@doc_subst(map_params_doc_snippets)
class Map(ConfigurationMixin, GMapsWidgetMixin, widgets.DOMWidget):
    """
    Base map class

    Instances of this act as a base map on which you can add
    additional layers.

    You should use the :func:`gmaps.figure` factory method
    to instiate a figure, rather than building this class
    directly.

    :param initial_viewport:
        Define the initial zoom level and map centre. You should
        construct this using one of the static methods on
        :class:`gmaps.InitialViewport`. By default, the
        map is centered on the data.

    {map_type}

    {mouse_handling}

    :Examples:

    >>> m = gmaps.Map()
    >>> m.add_layer(gmaps.heatmap_layer(locations))

    To explicitly set the initial map zoom and center:

    >>> zoom_level = 8
    >>> center = (20.0, -10.0)
    >>> viewport = InitialViewport.from_zoom_center(zoom_level, center)
    >>> m = gmaps.Map(initial_viewport=viewport)

    To have a satellite map:

    >>> m = gmaps.Map(map_type='HYBRID')

    You can also change this dynamically:

    >>> m.map_type = 'TERRAIN'
    """
    _view_name = Unicode('PlainmapView').tag(sync=True)
    _model_name = Unicode('PlainmapModel').tag(sync=True)
    layers = Tuple(trait=Instance(widgets.Widget)).tag(
        sync=True, **widgets.widget_serialization)
    data_bounds = List(DEFAULT_BOUNDS).tag(sync=True)
    initial_viewport = InitialViewport(default_value='DATA_BOUNDS').tag(
            sync=True, to_json=_serialize_viewport)
    map_type = MapType('ROADMAP').tag(sync=True)
    tilt = Tilt().tag(sync=True)
    mouse_handling = MouseHandling('COOPERATIVE').tag(sync=True)

    def add_layer(self, layer):
        self.layers = tuple([l for l in self.layers] + [layer])

    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    @observe('layers')
    def _calc_bounds(self, change):
        layers = change['new']
        bounds_list = [
            layer.data_bounds for layer in layers if layer.has_bounds
        ]
        if bounds_list:
            min_latitude = min(bounds[0][0] for bounds in bounds_list)
            max_latitude = max(bounds[1][0] for bounds in bounds_list)

            longitude_bounds = [
                (bounds[0][1], bounds[1][1]) for bounds in bounds_list
            ]
            min_longitude, max_longitude =\
                merge_longitude_bounds(longitude_bounds)

            self.data_bounds = [
                (min_latitude, min_longitude),
                (max_latitude, max_longitude)
            ]
