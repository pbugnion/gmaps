
import ipywidgets as widgets
from traitlets import (Unicode, CUnicode, default, Int,
                       List, Tuple, Float, Instance, validate)

import geotraitlets

DEFAULT_CENTER = (46.2, 6.1)

class InvalidPointException(Exception):
    pass

class Plainmap(widgets.DOMWidget):
    _view_name = Unicode("PlainmapView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("PlainmapModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    zoom = Int(8).tag(sync=True)
    center = geotraitlets.Point(DEFAULT_CENTER).tag(sync=True)
    layers = Tuple(trait=Instance(widgets.Widget)).tag(sync=True, **widgets.widget_serialization)

    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')


class HeatmapLayer(widgets.Widget):
    _view_name = Unicode("HeatmapLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("HeatmapLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List().tag(sync=True)
    max_intensity = Float(default_value=None, allow_none=True).tag(sync=True)
    point_radius = Float(default_value=None, allow_none=True).tag(sync=True)

    @validate("data")
    def _validate_data(self, proposal):
        for point in proposal["value"]:
            if not geotraitlets.is_valid_point(point):
                raise InvalidPointException(
                    "{} is not a valid latitude, longitude pair".format(point))
        return proposal["value"]


def plainmap():
    return Plainmap()


def heatmap(data):
    p = Plainmap()
    heatmap_layer = HeatmapLayer()
    heatmap_layer.data = data
    p.layers = (heatmap_layer, )
    return p
