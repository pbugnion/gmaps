import ipywidgets as widgets
from traitlets import Unicode


class Transit(widgets.Widget):
    _view_name = Unicode('TransitLayerView').tag(sync=True)
    _view_module = Unicode('jupyter-gmaps').tag(sync=True)
    _model_name = Unicode('TransitLayerModel').tag(sync=True)
    _model_module = Unicode('jupyter-gmaps').tag(sync=True)
    has_bounds = False
