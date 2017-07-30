import ipywidgets as widgets
from traitlets import Unicode

class Bicycling(widgets.Widget):
    _view_name = Unicode('BicyclingLayerView').tag(sync=True)
    _view_module = Unicode('jupyter-gmaps').tag(sync=True)
    _model_name = Unicode('BicyclingLayerModel').tag(sync=True)
    _model_module = Unicode('jupyter-gmaps').tag(sync=True)
    has_bounds = False


def bicycling_layer():
    return Bicycling()
