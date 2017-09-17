
import copy
import collections

import ipywidgets as widgets

from traitlets import (
    Unicode, List, Enum, Instance,
    Bool, default, observe
)

from .maps import GMapsWidgetMixin
from .marker import Marker, MarkerOptions


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
    features = List().tag(sync=True, **widgets.widget_serialization)
    mode = Enum(
        ALLOWED_DRAWING_MODES,
        default_value=DEFAULT_DRAWING_MODE
    ).tag(sync=True)
    marker_options = Instance(MarkerOptions, allow_none=False)
    toolbar_controls = Instance(DrawingControls, allow_none=False).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        self._new_marker_callbacks = []

        super(Drawing, self).__init__(**kwargs)
        self.on_msg(self._handle_message)

        # Observe all changes to the marker_options
        # to let users change these directly
        # and still trigger appropriate changes
        self.marker_options.observe(self._on_marker_options_change)

    def on_new_marker(self, callback):
        self._new_marker_callbacks.append(callback)

    def _on_marker_options_change(self, change):
        self.marker_options = copy.deepcopy(self.marker_options)

    @default('marker_options')
    def _default_marker_options(self):
        return MarkerOptions()

    @default('toolbar_controls')
    def _default_toolbar_controls(self):
        return DrawingControls()

    @observe('features')
    def _on_new_overlay(self, change):
        if self._new_marker_callbacks:
            old_features = change['old']
            new_features = change['new']
            old_markers = set([
                feature for feature in old_features
                if isinstance(feature, Marker)
            ])
            new_markers = [
                feature for feature in new_features
                if isinstance(feature, Marker)
                and feature not in old_markers
            ]
            for marker in new_markers:
                for callback in self._new_marker_callbacks:
                    callback(marker)

    def _handle_message(self, _, content, buffers):
        if content.get('event') == 'FEATURE_ADDED':
            payload = content['payload']
            latitude = payload['latitude']
            longitude = payload['longitude']
            marker = self.marker_options.to_marker(latitude, longitude)
            self.features = self.features + [marker]
        elif content.get('event') == 'MODE_CHANGED':
            payload = content['payload']
            mode = payload['mode']
            self.mode = mode


def _marker_options_from_dict(options_dict):
    return MarkerOptions(**options_dict)


def drawing_layer(
        features=None, mode=DEFAULT_DRAWING_MODE, 
        show_controls=True, marker_options=None):
    """
    Create an interactive drawing layer
    """
    if features is None:
        features = []
    controls = DrawingControls(show_controls=show_controls)
    if marker_options is None:
        marker_options = MarkerOptions()
    elif isinstance(marker_options, collections.Mapping):
        marker_options = _marker_options_from_dict(marker_options)
    kwargs = {
        'features': features,
        'mode': mode,
        'toolbar_controls': controls,
        'marker_options': marker_options
    }
    return Drawing(**kwargs)
