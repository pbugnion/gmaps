
import ipywidgets as widgets
from traitlets import Unicode, Dict, List


__all__ = ["GeoJson"]


class GeoJson(widgets.Widget):
    _view_name = Unicode("GeoJsonLayerView").tag(sync=True)
    _model_name = Unicode("GeoJsonLayerModel").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    has_bounds = False
    data = Dict().tag(sync=True)
    styles = List().tag(sync=True)
