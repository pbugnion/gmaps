
import ipywidgets as widgets

from traitlets import Unicode, List

from .maps import GMapsWidgetMixin


class Toolbar(GMapsWidgetMixin, widgets.DOMWidget):
    _view_name = Unicode("ToolbarView").tag(sync=True)
    _model_name = Unicode("ToolbarModel").tag(sync=True)
    layer_controls = List().tag(
        sync=True, **widgets.widget_serialization)

    def add_controls(self, controls):
        self.layer_controls = list(self.layer_controls) + [controls]
