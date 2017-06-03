
import ipywidgets as widgets

from traitlets import Unicode, List


class ErrorsBox(widgets.DOMWidget):
    """
    Box to hold any JS errors that occur
    """
    _view_name = Unicode("ErrorsBoxView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("ErrorsBoxModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    errors = List(trait=Unicode).tag(sync=True)
