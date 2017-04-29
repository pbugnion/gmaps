
import ipywidgets as widgets

from traitlets import Unicode


class Toolbar(widgets.DOMWidget):
    _view_name = Unicode("ToolbarView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("ToolbarModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
