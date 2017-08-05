
import ipywidgets as widgets

from traitlets import Unicode

from .maps import GMapsWidgetMixin


class Toolbar(GMapsWidgetMixin, widgets.DOMWidget):
    _view_name = Unicode("ToolbarView").tag(sync=True)
    _model_name = Unicode("ToolbarModel").tag(sync=True)
