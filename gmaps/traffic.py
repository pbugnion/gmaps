import ipywidgets as widgets

from traitlets import Unicode

from .maps import GMapsWidgetMixin


class Traffic(GMapsWidgetMixin, widgets.Widget):
    """
    Traffic layer
    """
    _view_name = Unicode('TrafficLayerView').tag(sync=True)
    _model_name = Unicode('TrafficLayerModel').tag(sync=True)
    has_bounds = False


def traffic_layer():
    """
    Traffic layer
    """
    return Traffic()