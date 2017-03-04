
import copy

import ipywidgets as widgets
from traitlets import (Unicode, Dict, List, observe)

import geojson

from . import bounds
from .options import merge_option_dicts

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


def geojson_layer(geojson, fill_color, stroke_color):
    styled_geojson = copy.deepcopy(geojson)
    style_options = {
        "fillColor": fill_color,
        "strokeColor": stroke_color
    }
    styles = merge_option_dicts(style_options)
    for feature, styles in zip(styled_geojson["features"], styles):
        feature["properties"]["style"] = styles
    return GeoJson(data=styled_geojson)
