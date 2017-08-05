
import ipywidgets as widgets

from traitlets import Unicode, List

from .maps import GMapsWidgetMixin


class ErrorsBox(GMapsWidgetMixin, widgets.DOMWidget):
    """
    Box to hold any JS errors that occur
    """
    _view_name = Unicode("ErrorsBoxView").tag(sync=True)
    _model_name = Unicode("ErrorsBoxModel").tag(sync=True)
    errors = List(trait=Unicode).tag(sync=True)
