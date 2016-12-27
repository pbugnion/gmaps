
import collections

from six import string_types
import ipywidgets as widgets
from traitlets import (
    Unicode, Int, List, observe, HasTraits, Float, Bool
)

import gmaps.geotraitlets as geotraitlets
import gmaps.bounds as bounds

from .maps import DEFAULT_CENTER

__all__ = ["Symbol", "Marker", "Markers", "marker_layer", "symbol_layer"]


class _BaseMarkerMixin(HasTraits):
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    location = geotraitlets.Point(DEFAULT_CENTER).tag(sync=True)
    hover_text = Unicode("").tag(sync=True)
    display_info_box = Bool(False).tag(sync=True)
    info_box_content = Unicode("").tag(sync=True)


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
    fill_opacity = Float(min=0.0, max=1.0, default_value=1.0).tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=True, default_value=None
    ).tag(sync=True)
    stroke_opacity = Float(min=0.0, max=1.0, default_value=1.0).tag(sync=True)
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
        isinstance(elem, string_types) or
        not isinstance(elem, collections.Iterable)
    )


def _is_color_atomic(color):
    """
    Determine whether the argument is a singe color or an iterable of colors
    """
    if isinstance(color, string_types):
        is_atomic = True
    elif isinstance(color, collections.Sequence):
        if isinstance(color[0], string_types):
            is_atomic = False
        elif isinstance(color[0], (int, float)) and len(color) in (3, 4):
            is_atomic = True
        else:
            is_atomic = False
    else:
        is_atomic = True
    return is_atomic


def _merge_option_dicts(option_dicts):
    """
    Create a list of options for marker and symbol layers

    This helper function takes a dictionary of (key -> list) and
    returns a list of dictionaries of (key -> value).
    """
    option_values_lengths = [
        len(option_values) for option_values in option_dicts.values()
    ]
    # assert all the list values are the same length
    number_items = option_values_lengths[0]
    assert all(
        length == number_items
        for length in option_values_lengths
    )
    option_lists = []
    for item in range(number_items):
        item_options = {
            option_name: option_values[item]
            for (option_name, option_values)
            in option_dicts.items()
        }
        option_lists.append(item_options)
    return option_lists


def _info_box_option_lists(number_markers, info_box_content, display_info_box):
    if _is_atomic(info_box_content):
        info_box_content = [info_box_content] * number_markers
    if _is_atomic(display_info_box):
        display_info_box = [display_info_box] * number_markers

    # Set value for display_info_box if it's still the default
    for imarker in range(number_markers):
        if display_info_box[imarker] is None:
            is_content_empty = (info_box_content[imarker] is None)
            if is_content_empty:
                display_info_box[imarker] = False
                info_box_content[imarker] = ""
            else:
                display_info_box[imarker] = True

    options = {
        "info_box_content": info_box_content,
        "display_info_box": display_info_box
    }
    return options


def _symbol_layer_options(
        locations, hover_text, fill_color, fill_opacity,
        stroke_color, stroke_opacity, scale,
        info_box_content, display_info_box):
    number_markers = len(locations)
    if _is_atomic(hover_text):
        hover_text = [hover_text] * number_markers
    if _is_atomic(scale):
        scale = [scale] * number_markers
    if _is_color_atomic(fill_color):
        fill_color = [fill_color] * number_markers
    if _is_color_atomic(stroke_color):
        stroke_color = [stroke_color] * number_markers
    if _is_atomic(stroke_opacity):
        stroke_opacity = [stroke_opacity] * number_markers
    if _is_atomic(fill_opacity):
        fill_opacity = [fill_opacity] * number_markers

    symbol_options = {
        "location": locations,
        "hover_text": hover_text,
        "fill_color": fill_color,
        "stroke_color": stroke_color,
        "scale": scale
    }

    info_box_options = _info_box_option_lists(
        number_markers, info_box_content, display_info_box)

    symbol_options.update(info_box_options)

    return _merge_option_dicts(symbol_options)


def _marker_layer_options(
        locations, hover_text, label, info_box_content, display_info_box):
    number_markers = len(locations)
    if _is_atomic(hover_text):
        hover_text = [hover_text] * number_markers
    if _is_atomic(label):
        label = [label] * number_markers
    if _is_atomic(info_box_content):
        info_box_content = [info_box_content] * number_markers

    marker_options = {
        "location": locations,
        "hover_text": hover_text,
        "label": label
    }

    info_box_options = _info_box_option_lists(
        number_markers, info_box_content, display_info_box)

    marker_options.update(info_box_options)

    return _merge_option_dicts(marker_options)


def symbol_layer(
        locations, hover_text="", fill_color=None,
        fill_opacity=1.0, stroke_color=None, stroke_opacity=1.0,
        scale=3, info_box_content=None, display_info_box=None):
    """
    Symbol layer

    Add this layer to a ``Map`` instance to draw symbols
    on the map. A symbol will be drawn on the map for each
    point in the ``locations`` argument.

    :Examples:

    >>> m = gmaps.Map()
    >>> locations = [
            (-34.0, -59.166672),
            (-32.23333, -64.433327),
            (40.166672, 44.133331),
            (51.216671, 5.0833302),
            (51.333328, 4.25)
        ]
    >>> symbols = gmaps.symbol_layer(
            locations, fill_color="red", stroke_color="red")
    >>> m.add_layer(symbols)

    You can set a list of information boxes, which will be displayed when the
    user clicks on a marker.

    >>> list_of_infoboxes = [
            "Simple string info box",
            "<a href='http://example.com'>HTML content</a>"
        ]
    >>> symbol_layer = gmaps.symbol_layer(
                locations, info_box_content=list_of_infoboxes)

    You can also set text that appears when someone's mouse hovers
    over a point:

    >>> names = ["Atucha", "Embalse", "Armenia", "BR", "Doel"]
    >>> symbol_layer = gmaps.symbol_layer(locations, hover_text=names)

    Apart from ``locations``, which must be an iterable of
    (latitude, longitude) pairs, the arguments can be given as
    either a list of the same length as ``locations``, or a
    single value. If given as a single value, this value will
    be broadcast to every marker. Thus, these two calls are equivalent:

    >>> symbols = gmaps.symbol_layer(
            locations, fill_color=["red"]*len(locations))
    >>> symbols = gmaps.symbol_layer(
            locations, fill_color="red")

    The former is useful for passing different colours to
    different symbols.

    >>> colors = ["red", "green", "blue", "black", "white"]
    >>> symbols = gmaps.symbol_layer(
            locations, fill_color=colors, stroke_color=colors)

    :param locations:
        List of (latitude, longitude) pairs
        denoting a single point. Latitudes are expressed as
        a float between -90 (corresponding to 90 degrees south)
        and +90 (corresponding to 90 degrees north). Longitudes
        are expressed as a float between -180 (corresponding to 180
        degrees west) and +180 (corresponding to 180 degrees east).
    :type locations: list of tuples

    :param hover_text:
        Text to be displayed when a user's mouse is hovering over
        a marker. This can be either a single string, in which case
        it will be applied to every marker, or a list of strings,
        in which case it must be of the same length as `locations`.
        If this is set to an empty string, nothing will appear when
        the user's mouse hovers over a symbol.
    :type hover_text: string or list of strings, optional

    :param fill_color:
        The fill color of the symbol. This can be specified as a
        single color, in which case the same color will apply to every symbol,
        or as a list of colors, in which case it must be the
        same length as ``locations``.
        Colors can be specified as a simple string, e.g. 'blue',
        as an RGB tuple, e.g. (100, 0, 0), or as an RGBA tuple, e.g.
        (100, 0, 0, 0.5).
    :type fill_color: single color or list of colors, optional

    :param fill_opacity:
        The opacity of the fill color. The opacity should be a float
        between 0.0 (transparent) and 1.0 (opaque), or a list of floats.
        1.0 by default.
    :type fill_opacity: float or list of floats, optional

    :param stroke_color:
        The stroke color of the symbol. This can be specified as a
        single color, in which case the same color will apply to every symbol,
        or as a list of colors, in which case it must be the
        same length as ``locations``.
        Colors can be specified as a simple string, e.g. 'blue',
        as an RGB tuple, e.g. (100, 0, 0), or as an RGBA tuple, e.g.
        (100, 0, 0, 0.5).
    :type stroke_color: single color or list of colors, optional

    :param stroke_opacity:
        The opacity of the stroke color. The opacity should be a float
        between 0.0 (transparent) and 1.0 (opaque), or a list of floats.
        1.0 by default.
    :type stroke_opacity: float or list of floats, optional

    :param scale:
        How large the marker is. This can either be a single integer,
        in which case the same scale will be applied to every marker,
        or it must be an iterable of the same length as ``locations``.
        The scale must be greater than 1. This defaults to 3.
    :type scale: integer or list of integers, optional

    :param info_box_content:
        Content to be displayed when user clicks on a marker. This should
        either be a single string, in which case the same content will apply to
        every marker, or a list of strings of the same length of the
        `locations` list.
    :type info_box_content: string or list of strings, optional

    :param display_info_box:
        Whether to display an info box when the user clicks on a symbol.
        This should either be a single boolean value, in which case it
        will be applied to every symbol, or a list of boolean values of the
        same length as the `locations` list.
        The default value is True for any symbols for which `info_box_content`
        is set, and False otherwise.
    :type display_info_box: boolean or list of booleans, optional
    """
    options = _symbol_layer_options(
        locations, hover_text, fill_color,
        fill_opacity, stroke_color, stroke_opacity, scale,
        info_box_content, display_info_box)
    symbols = [Symbol(**option) for option in options]
    return Markers(markers=symbols)


def marker_layer(
        locations, hover_text="", label="",
        info_box_content=None, display_info_box=None):
    """
    Marker layer

    Add this layer to a ``Map`` instance to draw markers
    corresponding to specific locations on the map.
    A marker will be drawn on teh map for each point in the
    ``locations`` argument.

    :Examples:

    >>> m = gmaps.Map()
    >>> locations = [
            (-34.0, -59.166672),
            (-32.23333, -64.433327),
            (40.166672, 44.133331),
            (51.216671, 5.0833302),
            (51.333328, 4.25)
        ]
    >>> symbols = gmaps.marker_layer(locations)
    >>> m.add_layer(symbols)

    :param locations:
        List of (latitude, longitude) pairs
        denoting a single point. Latitudes are expressed as
        a float between -90 (corresponding to 90 degrees south)
        and +90 (corresponding to 90 degrees north). Longitudes
        are expressed as a float between -180 (corresponding to 180
        degrees west) and +180 (corresponding to 180 degrees east).
    :type locations: list of tuples

    :param hover_text:
        Text to be displayed when a user's mouse is hovering over
        a marker. This can be either a single string, in which case
        it will be applied to every marker, or a list of strings,
        in which case it must be of the same length as `locations`.
        If this is set to an empty string, nothing will appear when
        the user's mouse hovers over a marker.
    :type hover_text: string or list of strings, optional

    :param label:
        Text to be displayed inside the marker. Google maps
        only displays the first letter of whatever string is
        passed to the marker.
        This can be either a single string, in which case
        every marker will receive the same label, or a list of
        strings, in which case it must be of the same length
        as `locations`.
    :type label: string or list of strings, optional

    :param info_box_content:
        Content to be displayed when user clicks on a marker. This should
        either be a single string, in which case the same content will apply to
        every marker, or a list of strings of the same length of the
        `locations` list.
    :type info_box_content: string or list of strings, optional

    :param display_info_box:
        Whether to display an info box when the user clicks on a marker.
        This should either be a single boolean value, in which case it
        will be applied to every marker, or a list of boolean values of the
        same length as the `locations` list.
        The default value is True for any markers for which `info_box_content`
        is set, and False otherwise.
    :type display_info_box: boolean or list of booleans, optional
    """
    marker_options = _marker_layer_options(
        locations, hover_text, label, info_box_content, display_info_box)
    markers = [Marker(**option) for option in marker_options]
    return Markers(markers=markers)
