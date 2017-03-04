
import copy

import ipywidgets as widgets
from traitlets import (Unicode, Dict, List, observe)

import geojson

from . import bounds
from .options import (
    merge_option_dicts, broadcast_if_atomic, broadcast_if_color_atomic)

__all__ = ["GeoJson", "geojson_layer"]


class GeoJson(widgets.Widget):
    _view_name = Unicode("GeoJsonLayerView").tag(sync=True)
    _model_name = Unicode("GeoJsonLayerModel").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    has_bounds = True
    data_bounds = List().tag(sync=True)
    data = Dict().tag(sync=True)

    def _set_bounds(self, data):
        longitudes, latitudes = [], []
        for feature in data["features"]:
            feature_coords = geojson.utils.coords(feature)
            feature_longitudes, feature_latitudes = zip(*feature_coords)
            longitudes.extend(feature_longitudes)
            latitudes.extend(feature_latitudes)
        min_latitude, max_latitude = bounds.latitude_bounds(latitudes)
        min_longitude, max_longitude = bounds.longitude_bounds(longitudes)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]

    @observe("data")
    def _calc_bounds(self, change):
        data = change["new"]
        self._set_bounds(data)


def _geojson_layer_options(
        number_features, hover_text, fill_color, fill_opacity,
        stroke_color, stroke_opacity, stroke_weight):
    style_options = {
        "title": broadcast_if_atomic(hover_text, number_features),
        "fillColor": broadcast_if_color_atomic(fill_color, number_features),
        "fillOpacity": broadcast_if_atomic(fill_opacity, number_features),
        "strokeColor":
            broadcast_if_color_atomic(stroke_color, number_features),
        "strokeOpacity": broadcast_if_atomic(stroke_opacity, number_features),
        "strokeWeight": broadcast_if_atomic(stroke_weight, number_features)
    }
    return merge_option_dicts(style_options)


def geojson_layer(
        geojson, hover_text="", fill_color=None,
        fill_opacity=0.4, stroke_color=None, stroke_opacity=0.8,
        stroke_weight=3.0):
    styled_geojson = copy.deepcopy(geojson)
    features = styled_geojson["features"]
    number_features = len(features)
    styles = _geojson_layer_options(
        number_features, hover_text, fill_color, fill_opacity, stroke_color,
        stroke_opacity, stroke_weight)
    for feature, style in zip(features, styles):
        feature["properties"]["style"] = style
    return GeoJson(data=styled_geojson)
