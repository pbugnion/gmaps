
import ipywidgets as widgets

from traitlets import Unicode, List, Enum, Instance, Bool, default

from .maps import GMapsWidgetMixin
from .marker import MarkerOptions


ALLOWED_DRAWING_MODES = {'DISABLED', 'MARKER'}
DEFAULT_DRAWING_MODE = 'MARKER'


class DrawingControls(GMapsWidgetMixin, widgets.DOMWidget):
    _model_name = Unicode('DrawingControlsModel').tag(sync=True)
    _view_name = Unicode('DrawingControlsView').tag(sync=True)
    show_controls = Bool(default_value=True, allow_none=False).tag(
        sync=True)


class Drawing(GMapsWidgetMixin, widgets.Widget):
    has_bounds = False
    _view_name = Unicode('DrawingLayerView').tag(sync=True)
    _model_name = Unicode('DrawingLayerModel').tag(sync=True)
    overlays = List().tag(sync=True, **widgets.widget_serialization)
    mode = Enum(
        ALLOWED_DRAWING_MODES,
        default_value=DEFAULT_DRAWING_MODE
    ).tag(sync=True)
    marker_options = Instance(MarkerOptions, allow_none=False)
    toolbar_controls = Instance(DrawingControls, allow_none=False).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(Drawing, self).__init__(**kwargs)
        self.on_msg(self._handle_message)

    @default('marker_options')
    def _default_marker_options(self):
        return MarkerOptions()

    @default('toolbar_controls')
    def _default_toolbar_controls(self):
        return DrawingControls()

    def _handle_message(self, _, content, buffers):
        if content.get('event') == 'OVERLAY_ADDED':
            payload = content['payload']
            latitude = payload['latitude']
            longitude = payload['longitude']
            marker = self.marker_options.to_marker(latitude, longitude)
            self.overlays = self.overlays + [marker]
        elif content.get('event') == 'MODE_CHANGED':
            payload = content['payload']
            mode = payload['mode']
            self.mode = mode
