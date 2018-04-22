
import json
import copy

import ipywidgets as widgets
from traitlets import (Unicode, Dict, List, observe, Float)

import geojson

from . import geotraitlets
from . import bounds
from .options import (
    merge_option_dicts, broadcast_if_atomic, broadcast_if_color_atomic)
from .maps import GMapsWidgetMixin

__all__ = ["GeoJson", "geojson_layer", "GeoJsonFeature", "InvalidGeoJson"]


class InvalidGeoJson(Exception):
    pass


class GeoJsonFeature(GMapsWidgetMixin, widgets.Widget):
    """
    Widget for a single GeoJSON feature.

    Prefer to use the `geojson_layer` function to construct these,
    rather than making them explicitly.
    """
    _view_name = Unicode("GeoJsonFeatureView").tag(sync=True)
    _model_name = Unicode("GeoJsonFeatureModel").tag(sync=True)
    feature = Dict().tag(sync=True)
    has_bounds = False
    fill_color = geotraitlets.ColorAlpha(
        allow_none=True, default_value=None
    ).tag(sync=True)
    fill_opacity = geotraitlets.Opacity(default_value=1.0).tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=True, default_value=None).tag(sync=True)
    stroke_opacity = geotraitlets.Opacity(default_value=1.0).tag(sync=True)
    stroke_weight = Float(min=0.0, default_value=1.0).tag(sync=True)

    def get_coords(self):
        return geojson.utils.coords(self.feature)


class GeoJson(GMapsWidgetMixin, widgets.Widget):
    """
    Widget for a collection of GeoJSON features.

    Prefer to use the `geojson_layer` function to construct this,
    rather than making them explicitly.

    Use the `features` attribute on this class to change the style
    of the features in this layer.
    """
    _view_name = Unicode("GeoJsonLayerView").tag(sync=True)
    _model_name = Unicode("GeoJsonLayerModel").tag(sync=True)
    has_bounds = True
    data_bounds = List().tag(sync=True)
    features = List().tag(sync=True, **widgets.widget_serialization)

    def _set_bounds(self, features):
        longitudes, latitudes = [], []
        for feature in features:
            feature_coords = feature.get_coords()
            feature_longitudes, feature_latitudes = zip(*feature_coords)
            longitudes.extend(feature_longitudes)
            latitudes.extend(feature_latitudes)
        min_latitude, max_latitude = bounds.latitude_bounds(latitudes)
        min_longitude, max_longitude = bounds.longitude_bounds(longitudes)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]

    @observe("features")
    def _calc_bounds(self, change):
        data = change["new"]
        self._set_bounds(data)


def _geojson_layer_options(
        number_features, fill_color, fill_opacity,
        stroke_color, stroke_opacity, stroke_weight):
    feature_options = {
        "fill_color": broadcast_if_color_atomic(fill_color, number_features),
        "fill_opacity": broadcast_if_atomic(fill_opacity, number_features),
        "stroke_color":
            broadcast_if_color_atomic(stroke_color, number_features),
        "stroke_opacity": broadcast_if_atomic(stroke_opacity, number_features),
        "stroke_weight": broadcast_if_atomic(stroke_weight, number_features)
    }
    return merge_option_dicts(feature_options)


def _validate_feature(feature):
    if feature.get("properties") is None:
        feature["properties"] = {}
    if feature.get('geometry') is None:
        raise InvalidGeoJson(
            "Feature with properties {} does not have a geometry.".format(
                feature.get("properties")))
    return feature


def _validate_geojson(geojson_document):
    try:
        geojson_instance = geojson.loads(json.dumps(geojson_document))
    except ValueError as e:
        raise InvalidGeoJson(e.message)
    if not isinstance(geojson_instance, geojson.GeoJSON):
        # Sometimes GeoJSON.to_instance fails silently and just returns
        # the original type, rather than validation errors.
        # Try with, e.g. an empty dictionary.
        raise InvalidGeoJson('Could not convert document to GeoJSON.')
    if not geojson_instance.is_valid:
        raise InvalidGeoJson(", ".join(geojson_instance.errors()))
    if geojson_document["type"] != "FeatureCollection":
        raise InvalidGeoJson(
            "Only FeatureCollection GeoJSON is currently supported")


def geojson_layer(
        geojson, fill_color=None,
        fill_opacity=0.4, stroke_color=None, stroke_opacity=0.8,
        stroke_weight=1.0):
    """
    GeoJSON layer

    Add this layer to a :class:`gmaps.Figure` instance to render GeoJSON.

    :Examples:

    Let's start by fetching some GeoJSON. We could have loaded it from file,
    but let's load it from a URL instead. You will need `requests`.

    >>> import json
    >>> import requests
    >>> countries_string = requests.get(
        "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    ).content
    >>> countries = json.loads(countries_string)

    >>> import gmaps
    >>> gmaps.configure(api_key="AI...")
    >>> fig = gmaps.figure()
    >>> geojson = gmaps.geojson_layer(countries)
    >>> fig.add_layer(geojson)
    >>> fig

    We can pass style options into the layer. Let's assign a random
    color to each country:

    >>> import random
    >>> colors = [
        random.choice(['red', 'green', 'blue', 'purple', 'yellow', 'teal'])
        for country in countries['features']
    ]
    >>> geojson = gmaps.geojson_layer(countries, fill_color=colors)

    Finally, let's also make our colors more transparent and decrease
    the stroke weight.

    >>> geojson = gmaps.geojson_layer(
            countries, fill_color=colors, fill_opacity=0.2, stroke_weight=1)

    :param geojson:
        A Python dictionary containing a GeoJSON feature collection. If you
        have a GeoJSON file, you will need to load it using
        `json.load <https://docs.python.org/3.6/library/json.html>`_.
    :type geojson: dict

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
        0.4 by default.
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
        0.8 by default.
    :type stroke_opacity: float or list of floats, optional

    :param stroke_weight:
        The width, in pixels, of the stroke. Useful values range from 0.0
        (corresponding to no stroke) to about 20, corresponding to a very
        fat brush. 3.0 by default.
    :type stroke_weight: float or list of floats, optional
    """
    _validate_geojson(geojson)
    styled_geojson = copy.deepcopy(geojson)
    raw_features = styled_geojson["features"]
    features = [_validate_feature(feature) for feature in raw_features]
    number_features = len(features)
    styles = _geojson_layer_options(
        number_features, fill_color, fill_opacity, stroke_color,
        stroke_opacity, stroke_weight)
    feature_widgets = []
    for feature, style in zip(features, styles):
        feature_widget = GeoJsonFeature(feature=feature, **style)
        feature_widgets.append(feature_widget)
    return GeoJson(features=feature_widgets)
