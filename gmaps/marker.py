
import ipywidgets as widgets
from traitlets import Unicode, Int, default, List, observe, HasTraits
import collections

import gmaps.geotraitlets as geotraitlets
import gmaps.bounds as bounds

from .maps import DEFAULT_CENTER

__all__ = ["Symbol", "Marker", "Markers", "marker_layer", "symbol_layer"]


class _BaseMarkerMixin(HasTraits):
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    location = geotraitlets.Point(DEFAULT_CENTER).tag(sync=True)
    hover_text = Unicode("").tag(sync=True)


class Symbol(_BaseMarkerMixin, widgets.Widget):
    """
    Class representing a single symbol.

    Symbols are like markers, but the point is represented by
    an SVG symbol, rather than the default inverted droplet.
    Symbols should be added to the map via the 'Markers'
    widget.
    """
    _view_name = Unicode("SymbolView").tag(sync=True)
    _model_name = Unicode("SymbolModel").tag(sync=True)

    fill_color = geotraitlets.ColorAlpha(
        allow_none=True, default_value=None
    ).tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=True, default_value=None
    ).tag(sync=True)
    scale = Int(
        default_value=4, allow_none=True, min=1
    ).tag(sync=True)


class Marker(_BaseMarkerMixin, widgets.Widget):
    """
    Class representing a marker.

    Markers should be added to the map via the 'Markers'
    widget.
    """
    _view_name = Unicode("MarkerView").tag(sync=True)
    _model_name = Unicode("MarkerModel").tag(sync=True)
    label = Unicode("").tag(sync=True)


class Markers(widgets.Widget):
    has_bounds = True
    _view_name = Unicode("MarkerLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("MarkerLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    markers = List(minlen=1).tag(sync=True,  **widgets.widget_serialization)
    data_bounds = List().tag(sync=True)

    @observe("markers")
    def _calc_bounds(self, change):
        markers = change["new"]
        locations = [marker.location for marker in markers]
        latitudes = [location[0] for location in locations]
        longitudes = [location[1] for location in locations]
        min_latitude, max_latitude = bounds.latitude_bounds(latitudes)
        min_longitude, max_longitude = bounds.longitude_bounds(longitudes)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]


def _is_atomic(elem):
    return (
        isinstance(elem, basestring) or
        not isinstance(elem, collections.Iterable)
    )

def _is_color_atomic(color):
    """
    Determine whether the argument is a singe color or an iterable of colors
    """
    if isinstance(color, basestring):
        is_atomic = True
    elif isinstance(color, collections.Sequence):
        if isinstance(color[0], basestring):
            is_atomic = False
        if isinstance(color[0], (int, float)) and len(color) in (3, 4):
            is_atomic = True
    else:
        is_atomic = True
    return is_atomic


def symbol_layer(locations, hover_text="", fill_color=None, stroke_color=None, scale=None):
    number_markers = len(locations)
    if _is_atomic(hover_text):
        hover_text = [hover_text] * number_markers
    if _is_atomic(scale):
        scale = [scale] * number_markers
    if _is_color_atomic(fill_color):
        fill_color = [fill_color] * number_markers
    if _is_color_atomic(stroke_color):
        stroke_color = [stroke_color] * number_markers
    symbols = [
        Symbol(
            location=location, hover_text=hover_text,
            fill_color=fill_color, stroke_color=stroke_color,
            scale=scale
        )
        for (location, hover_text, scale, fill_color, stroke_color) in
        zip(locations, hover_text, scale, fill_color, stroke_color)
    ]
    return Markers(markers=symbols)


def marker_layer(locations, hover_text="", label=""):
    number_markers = len(locations)
    if _is_atomic(hover_text):
        hover_text = [hover_text] * number_markers
    if _is_atomic(label):
        label = [label] * number_markers
    markers = [
        Marker(location=location, hover_text=hover_text, label=label)
        for (location, hover_text, label) in
        zip(locations, hover_text, label)
    ]
    return Markers(markers=markers)
