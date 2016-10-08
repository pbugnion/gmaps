
import warnings

import ipywidgets as widgets
from traitlets import (Unicode, CUnicode, default, Bool,
                       List, Tuple, Float, Instance, validate,
                       observe, Dict, HasTraits)

import gmaps.geotraitlets as geotraitlets
import gmaps.bounds as bounds

DEFAULT_CENTER = (46.2, 6.1)
DEFAULT_BOUNDS = [(46.2, 6.1), (47.2, 7.1)]

_default_configuration = {"api_key": None}


def configure(api_key=None):
    """
    Configure access to the GoogleMaps API.

    :param api_key: String denoting the key to use when accessing Google maps,
        or None to not pass an API key.
    """
    configuration = {"api_key": api_key}
    global _default_configuration
    _default_configuration = configuration


class ConfigurationMixin(HasTraits):
    configuration = Dict(
        traits={"api_key": Unicode(allow_none=True)}).tag(sync=True)

    @default("configuration")
    def _config_default(self):
        return _default_configuration


class InvalidPointException(Exception):
    pass


class DirectionsServiceException(RuntimeError):
    pass


class Map(widgets.DOMWidget, ConfigurationMixin):
    """
    Base map class

    Instances of this act as a base map on which you can add
    additional layers.

    :Examples:

    >>> m = gmaps.Map()
    >>> m.add_layer(gmaps.Heatmap(data=data))
    """
    _view_name = Unicode("PlainmapView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("PlainmapModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    layers = Tuple(trait=Instance(widgets.Widget)).tag(
        sync=True, **widgets.widget_serialization)
    data_bounds = List(DEFAULT_BOUNDS).tag(sync=True)

    def add_layer(self, layer):
        self.layers = tuple([l for l in self.layers] + [layer])

    @default("layout")
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    @observe("layers")
    def _calc_bounds(self, change):
        layers = change["new"]
        bounds_list = [
            layer.data_bounds for layer in layers if layer.has_bounds
        ]
        if bounds_list:
            min_latitude = min(bounds[0][0] for bounds in bounds_list)
            min_longitude = min(bounds[0][1] for bounds in bounds_list)
            max_latitude = min(bounds[1][0] for bounds in bounds_list)
            max_longitude = min(bounds[1][1] for bounds in bounds_list)
            self.data_bounds = [
                (min_latitude, min_longitude),
                (max_latitude, max_longitude)
            ]


class Directions(widgets.Widget):
    """
    Directions layer.

    Add this to a ``Map`` instance to draw directions.

    By default, the directions are requested with the DRIVING option.

    Data is a list of lat,lon tuples. The first point of the list is passed as
    the origin of the itinerary; the last point is passed as the destination of
    the itinerary. Other points are passed in order as a list of waypoints.

    To set the parameters, pass them to the constructor:
    >>> directions_layer = gmaps.Directions(data=data)

    Examples:
    >>> m = gmaps.Map()
    >>> data = [(48.85341, 2.3488), (50.85045, 4.34878), (52.37403, 4.88969)]
    >>> directions_layer = gmaps.Directions(data=data)
    >>> m.add_layer(directions_layer)

    An TraitError is raised if you try to pass less than two points:
    >>> directions_layer = gmaps.Directions(data=[(50.0, 4.0])
    Traceback (most recent call last):
        ...
    TraitError: The 'data' trait of a Directions instance must be of
    length 2 <= L <= 9223372036854775807, but a value of [[50.0, 4.0]]
    was specified.

    There is a limitation in the number of waypoints allowed by Google. If it
    fails to return directions, a DirectionsServiceException is raised.
    >>> directions_layer = gmaps.Directions(data=data*10)
    Traceback (most recent call last):
        ...
    DirectionsServiceException: No directions returned: MAX WAYPOINTS EXCEEDED

    """
    has_bounds = True
    _view_name = Unicode("DirectionsLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("DirectionsLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List(minlen=2).tag(sync=True)
    data_bounds = List().tag(sync=True)

    layer_status = CUnicode().tag(sync=True)

    @validate("data")
    def _validate_data(self, proposal):
        for point in proposal["value"]:
            if not geotraitlets.is_valid_point(point):
                raise InvalidPointException(
                    "{} is not a valid latitude, longitude pair".format(point))
        return proposal["value"]

    @observe("data")
    def _calc_bounds(self, change):
        data = change["new"]
        min_latitude = min(row[0] for row in data)
        min_longitude = min(row[1] for row in data)
        max_latitude = max(row[0] for row in data)
        max_longitude = max(row[1] for row in data)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]

    @observe("layer_status")
    def _handle_layer_status(self, change):
        if change["new"] != "OK":
            raise DirectionsServiceException(
                "No directions returned: " + change["new"])


# Mixin for options common to both heatmap and weighted heatmaps.
class _HeatmapOptionsMixin(HasTraits):
    """
    :param max_intensity:
        Strictly positive floating point number indicating the numeric value
        that corresponds to the hottest colour in the heatmap gradient. Any
        density of points greater than that value will just get mapped to
        the hottest colour. Setting this value can be useful when your data
        is sharply peaked. It is also useful if you find that your heatmap
        disappears as you zoom in.
    :type max_intensity: float, optional

    :param point_radius:
        Number of pixels for each point passed in the data. This determines the
        "radius of influence" of each data point.
    :type point_radius: int, optional

    :param dissipating:
        Whether the radius of influence of each point changes as you zoom in
        or out. If `dissipating` is True, the radius of influence of each
        point increases as you zoom out and decreases as you zoom in. If
        False, the radius of influence remains the same. Defaults to True.
    :type dissipating: bool, optional

    :param opacity:
        The opacity of the heatmap layer. Defaults to 0.6.
    :type opacity: float, optional

    :param gradient:
        The color gradient for the heatmap. This must be specified as a list
        of colors. Google Maps then interpolates linearly between those
        colors.
        Colors can be specified as a simple string, e.g. 'blue',
        as an RGB tuple, e.g. (100, 0, 0), or as an RGBA tuple, e.g.
        (100, 0, 0, 0.5).
    :type gradient: list of colors, optional
    """
    max_intensity = Float(default_value=None, allow_none=True).tag(sync=True)
    point_radius = Float(default_value=None, allow_none=True).tag(sync=True)
    dissipating = Bool(default_value=True).tag(sync=True)
    opacity = Float(default_value=0.6, min=0.0, max=1.0).tag(sync=True)
    gradient = List(
        trait=geotraitlets.ColorAlpha(), allow_none=True, minlen=1
    ).tag(sync=True)

    @default("gradient")
    def _default_gradient(self):
        return None

    def set_bounds(self, data):
        latitudes = [row[0] for row in data]
        longitudes = [row[1] for row in data]
        min_latitude, max_latitude = self._latitude_bounds(latitudes)
        min_longitude, max_longitude = self._longitude_bounds(longitudes)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]

    def _latitude_bounds(self, latitudes):
        return bounds.latitude_bounds(latitudes)

    def _longitude_bounds(self, longitudes):
        return bounds.longitude_bounds(longitudes)


class Heatmap(widgets.Widget, _HeatmapOptionsMixin):
    __doc__ = """
    Heatmap layer.

    Add this to a ``Map`` instance to draw a heatmap. A heatmap shows
    the density of points in or near a particular area.

    To set the parameters, pass them to the constructor or set them
    on the heatmap object after construction::

    >>> heatmap_layer = gmaps.Heatmap(data=data, max_intensity=10)

    or::

    >>> heatmap_layer = gmaps.Heatmap()
    >>> heatmap_layer.data = data
    >>> heatmap_layer.max_intensity = 10

    :Examples:

    >>> m = gmaps.Map()
    >>> data = [(46.1, 5.2), (46.2, 5.3), (46.3, 5.4)]
    >>> heatmap_layer = gmaps.Heatmap(data=data)
    >>> heatmap_layer.max_intensity = 2
    >>> heatmap_layer.point_radius = 3
    >>> heatmap_layer.gradient = ['white', 'gray']
    >>> m.add_layer(heatmap_layer)

    :param data: List of (latitude, longitude) pairs denoting a single
        point. Latitudes are expressed as a float between -90
        (corresponding to 90 degrees south) and +90 (corresponding to
        90 degrees north). Longitudes are expressed as a float
        between -180 (corresponding to 180 degrees west) and 180
        (corresponding to 180 degrees east).
    :type data: list of tuples

    """ + _HeatmapOptionsMixin.__doc__
    has_bounds = True
    _view_name = Unicode("SimpleHeatmapLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("SimpleHeatmapLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List().tag(sync=True)
    data_bounds = List().tag(sync=True)

    @validate("data")
    def _validate_data(self, proposal):
        for point in proposal["value"]:
            if not geotraitlets.is_valid_point(point):
                raise InvalidPointException(
                    "{} is not a valid latitude, longitude pair".format(point))
        return proposal["value"]

    @observe("data")
    def _calc_bounds(self, change):
        data = change["new"]
        self.set_bounds(data)


class WeightedHeatmap(widgets.Widget, _HeatmapOptionsMixin):
    __doc__ = """
    Heatmap with weighted points.

    Add this layer to a ``Map`` instance to draw a heatmap. Unlike the plain
    Heatmap layer, which assumes that all points should have equal weight,
    this layer lets you specifiy different weights for points.

    :Examples:

    >>> m = gmaps.Map()
    # triples representing `latitude, longitude, weight`:
    >>> data = [(46.1, 5.2, 0.5), (46.2, 5.3, 0.2), (46.3, 5.4, 0.8)]
    >>> heatmap_layer = gmaps.Heatmap(data=data)
    >>> heatmap_layer.max_intensity = 2
    >>> m.add_layer(heatmap_layer)

    :param data: List of (latitude, longitude, weight) triples for a single
        point. Latitudes are expressed as a float between -90 (corresponding to
        90 degrees south) and +90 (corresponding to 90 degrees north).
        Longitudes are expressed as a float between -180
        (corresponding to 180 degrees west) and +180 (corresponding to
        180 degrees east). Weights must be non-negative.
    :type data: list of tuples

    """ + _HeatmapOptionsMixin.__doc__
    has_bounds = True
    _view_name = Unicode("WeightedHeatmapLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("WeightedHeatmapLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List().tag(sync=True)
    data_bounds = List().tag(sync=True)

    @validate("data")
    def _validate_data(self, proposal):
        for point in proposal["value"]:
            if not geotraitlets.is_valid_point(point[:2]):
                raise InvalidPointException(
                    "{} is not a valid latitude, longitude pair".format(point))
            # check weight
        return proposal["value"]

    @observe("data")
    def _calc_bounds(self, change):
        data = change["new"]
        self.set_bounds(data)


def plainmap():
    warnings.warn(
        "plainmap is deprecated. Prefer the Map class.",
        category=RuntimeWarning)
    return Map()


def heatmap(data):
    warnings.warn(
        "heatmap is deprecated. Prefer combining the Map class "
        "with a Heatmap layer",
        category=RuntimeWarning)
    p = Map()
    heatmap_layer = Heatmap()
    heatmap_layer.data = data
    p.layers = (heatmap_layer, )
    return p
