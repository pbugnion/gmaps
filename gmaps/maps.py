
import warnings

import ipywidgets as widgets
from traitlets import (Unicode, CUnicode, default, Int,
                       List, Tuple, Float, Instance, validate,
                       observe)

import gmaps.geotraitlets as geotraitlets

DEFAULT_CENTER = (46.2, 6.1)
DEFAULT_BOUNDS = [(46.2, 6.1), (47.2, 7.1)]

class InvalidPointException(Exception):
    pass

class Map(widgets.DOMWidget):
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
    layers = Tuple(trait=Instance(widgets.Widget)).tag(sync=True, **widgets.widget_serialization)
    data_bounds = List(DEFAULT_BOUNDS).tag(sync=True)

    def add_layer(self, layer):
        self.layers = tuple([layer for layer in self.layers] + [layer])

    @default("layout")
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    @observe("layers")
    def _calc_bounds(self, change):
        layers = change["new"]
        bounds_list = [layer.data_bounds for layer in layers if layer.has_bounds]
        if bounds_list:
            min_latitude = min(bounds[0][0] for bounds in bounds_list)
            min_longitude = min(bounds[0][1] for bounds in bounds_list)
            max_latitude = min(bounds[1][0] for bounds in bounds_list)
            max_longitude = min(bounds[1][1] for bounds in bounds_list)
            self.data_bounds = [(min_latitude, min_longitude), (max_latitude, max_longitude)]


class Heatmap(widgets.Widget):
    """
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
    >>> m.add_layer(heatmap_layer)

    :param data: List of (latitude, longitude) pairs denoting a single
        point. Latitudes
        are expressed as a float between -90 (corresponding to 90 degrees south)
        and 90 (corresponding to 90 degrees north). Longitudes are expressed
        as a float between -180 (corresponding to 180 degrees west) and 180
        (corresponding to 180 degrees east).
    :type data: list of tuples, optional

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
    """
    has_bounds = True
    _view_name = Unicode("SimpleHeatmapLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("SimpleHeatmapLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List().tag(sync=True)
    max_intensity = Float(default_value=None, allow_none=True).tag(sync=True)
    point_radius = Float(default_value=None, allow_none=True).tag(sync=True)
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
        min_latitude = min(row[0] for row in data)
        min_longitude = min(row[1] for row in data)
        max_latitude = max(row[0] for row in data)
        max_longitude = max(row[1] for row in data)
        self.data_bounds = [(min_latitude, min_longitude), (max_latitude, max_longitude)]


class WeightedHeatmap(widgets.Widget):
    has_bounds = True
    _view_name = Unicode("WeightedHeatmapLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("WeightedHeatmapLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List().tag(sync=True)
    max_intensity = Float(default_value=None, allow_none=True).tag(sync=True)
    point_radius = Float(default_value=None, allow_none=True).tag(sync=True)
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
        min_latitude = min(row[0] for row in data)
        min_longitude = min(row[1] for row in data)
        max_latitude = max(row[0] for row in data)
        max_longitude = max(row[1] for row in data)
        self.data_bounds = [(min_latitude, min_longitude), (max_latitude, max_longitude)]


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
    heatmap_layer = HeatmapLayer()
    heatmap_layer.data = data
    p.layers = (heatmap_layer, )
    return p
