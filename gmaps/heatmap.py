
import ipywidgets as widgets
from traitlets import (
    Float, Bool, Unicode, HasTraits, default, List, observe
)

from . import bounds
from .locations import locations_docstring
from . import geotraitlets
from .maps import GMapsWidgetMixin
from ._docutils import doc_subst


_doc_snippets = {}
_doc_snippets['locations'] = locations_docstring

_doc_snippets['options'] = """
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


# Mixin for options common to both heatmap and weighted heatmaps.
class _HeatmapOptionsMixin(HasTraits):
    max_intensity = Float(default_value=None, allow_none=True).tag(sync=True)
    point_radius = Float(default_value=None, allow_none=True).tag(sync=True)
    dissipating = Bool(default_value=True).tag(sync=True)
    opacity = Float(default_value=0.6, min=0.0, max=1.0).tag(sync=True)
    gradient = List(
        trait=geotraitlets.ColorAlpha(), allow_none=True, minlen=1
    ).tag(sync=True)

    @default('gradient')
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


@doc_subst(_doc_snippets)
class Heatmap(GMapsWidgetMixin, widgets.Widget, _HeatmapOptionsMixin):
    """
    Heatmap layer.

    Add this to a ``Map`` instance to draw a heatmap. A heatmap shows
    the density of points in or near a particular area.

    You should not instantiate this directly. Instead, use the
    :func:`gmaps.heatmap_layer` factory function.

    {locations}

    {options}

    :param data: DEPRECATED. Use `locations` instead.
        List of (latitude, longitude) pairs denoting a single
        point. Latitudes are expressed as a float between -90
        (corresponding to 90 degrees south) and +90 (corresponding to
        90 degrees north). Longitudes are expressed as a float
        between -180 (corresponding to 180 degrees west) and 180
        (corresponding to 180 degrees east).
    :type data: list of tuples

    :Examples:

    >>> fig = gmaps.figure()
    >>> locations = [(46.1, 5.2), (46.2, 5.3), (46.3, 5.4)]
    >>> heatmap = gmaps.heatmap_layer(locations)
    >>> heatmap.max_intensity = 2
    >>> heatmap.point_radius = 3
    >>> heatmap.gradient = ['white', 'gray']
    >>> fig.add_layer(heatmap_layer)
    """
    has_bounds = True
    _view_name = Unicode('SimpleHeatmapLayerView').tag(sync=True)
    _model_name = Unicode('SimpleHeatmapLayerModel').tag(sync=True)

    locations = geotraitlets.LocationArray(
        allow_none=False, minlen=1
    ).tag(sync=True)
    data_bounds = List().tag(sync=True)

    @observe('locations')
    def _calc_bounds(self, change):
        data = change['new']
        self.set_bounds(data)


@doc_subst(_doc_snippets)
class WeightedHeatmap(GMapsWidgetMixin, widgets.Widget, _HeatmapOptionsMixin):
    """
    Heatmap with weighted points.

    Add this layer to a ``Map`` instance to draw a heatmap. Unlike the plain
    Heatmap layer, which assumes that all points should have equal weight,
    this layer lets you specifiy different weights for points.

    You should not instantiate this directly. Instead, use the
    :func:`gmaps.heatmap_layer` factory function, passing in a
    parameter for `weights`.

    {locations}

    :param weights:
        List of non-negative floats corresponding to the importance of
        each latitude-longitude pair. Must have the same length as
        `locations`.
    :type weights: list of floats

    {options}

    :param data: DEPRECATED. Use `locations` and `weights` instead.
        List of (latitude, longitude, weight) triples for a single
        point. Latitudes are expressed as a float between -90 (corresponding to
        90 degrees south) and +90 (corresponding to 90 degrees north).
        Longitudes are expressed as a float between -180
        (corresponding to 180 degrees west) and +180 (corresponding to
        180 degrees east). Weights must be non-negative.
    :type data: list of tuples

    :Examples:

    >>> fig = gmaps.figure()
    >>> locations = [(46.1, 5.2), (46.2, 5.3), (46.3, 5.4)]
    >>> weights = [0.5, 0.2, 0.8]
    >>> heatmap = gmaps.heatmap_layer(locations, weights=weights)
    >>> heatmap.max_intensity = 2
    >>> fig.add_layer(heatmap_layer)
    """
    has_bounds = True
    _view_name = Unicode('WeightedHeatmapLayerView').tag(sync=True)
    _model_name = Unicode('WeightedHeatmapLayerModel').tag(sync=True)

    locations = geotraitlets.LocationArray(
        allow_none=False, minlen=1
    ).tag(sync=True)
    weights = geotraitlets.WeightArray(
        allow_none=False, minlen=1
    ).tag(sync=True)
    data_bounds = List().tag(sync=True)

    @observe('locations')
    def _calc_bounds(self, change):
        data = change['new']
        self.set_bounds(data)


def _heatmap_options(
        locations, weights, max_intensity, dissipating, point_radius,
        opacity, gradient):
    options = {
        'max_intensity': max_intensity,
        'dissipating': dissipating,
        'point_radius': point_radius,
        'opacity': opacity,
        'gradient': gradient
    }
    if weights is None:
        is_weighted = False
        widget_args = {'locations': locations}
    else:
        if len(weights) != len(locations):
            raise ValueError(
                'weights must be of the same length as locations or None')
        is_weighted = True
        widget_args = {
            'locations': locations,
            'weights': weights
        }
    widget_args.update(options)
    return widget_args, is_weighted


@doc_subst(_doc_snippets)
def heatmap_layer(
        locations, weights=None, max_intensity=None,
        dissipating=True, point_radius=None,
        opacity=0.6, gradient=None):
    """
    Create a heatmap layer.

    This returns a :class:`gmaps.Heatmap` or a :class:`gmaps.WeightedHeatmap`
    object that can be added to a :class:`gmaps.Figure` to draw a
    heatmap. A heatmap shows the density of points in or near
    a particular area.

    To set the parameters, pass them to the constructor or set
    them on the ``Heatmap`` object after construction::

    >>> heatmap = gmaps.heatmap_layer(locations, max_intensity=10)

    or::

    >>> heatmap = gmaps.heatmap_layer(locations)
    >>> heatmap.max_intensity = 10

    :Examples:

    >>> fig = gmaps.figure()
    >>> locations = [(46.1, 5.2), (46.2, 5.3), (46.3, 5.4)]
    >>> heatmap = gmaps.heatmap_layer(locations)
    >>> heatmap.max_intensity = 2
    >>> heatmap.point_radius = 3
    >>> heatmap.gradient = ['white', 'gray']
    >>> fig.add_layer(heatmap)

    {locations}

    :param weights:
        Iterable of weights of the same length as `locations`.
        All the weights must be positive.
    :type weights: iterable of floats, optional

    {options}

    :returns:
        A :class:`gmaps.Heatmap` or a :class:`gmaps.WeightedHeatmap` widget.
    """
    widget_args, is_weighted = _heatmap_options(
        locations, weights, max_intensity, dissipating, point_radius,
        opacity, gradient
    )
    if is_weighted:
        return WeightedHeatmap(**widget_args)
    else:
        return Heatmap(**widget_args)
