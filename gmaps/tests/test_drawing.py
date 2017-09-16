
import unittest

from .. import drawing, marker


class UnaryFunctionMock():
    """
    Simple mock for functions that take a single argument
    """

    def __init__(self):
        self.calls = []

    def __call__(self, arg):
        self.calls.append(arg)


class Drawing(unittest.TestCase):

    def test_default_overlays(self):
        layer = drawing.Drawing()
        assert layer.get_state()['overlays'] == []

    def test_with_overlays(self):
        marker_widget = marker.Marker()
        layer = drawing.Drawing(overlays=[marker_widget])
        overlays = layer.get_state()['overlays']
        assert len(overlays) == 1
        [serialized_marker] = overlays
        expected = 'IPY_MODEL_{}'.format(marker_widget.model_id)
        assert serialized_marker == expected

    def test_adding_marker(self):
        layer = drawing.Drawing()
        message = {
            'event': 'OVERLAY_ADDED',
            'payload': {
                'overlayType': 'MARKER',
                'latitude': 25.0,
                'longitude': -5.0
            }
        }
        layer._handle_custom_msg(message, None)
        assert len(layer.overlays) == 1
        [new_marker] = layer.overlays
        assert new_marker.location == (25.0, -5.0)

    def test_default_mode(self):
        layer = drawing.Drawing()
        assert layer.get_state()['mode'] == drawing.DEFAULT_DRAWING_MODE

    def test_changing_mode(self):
        layer = drawing.Drawing(mode='DISABLED')
        assert layer.get_state()['mode'] == 'DISABLED'

    def test_receiving_mode_changes(self):
        layer = drawing.Drawing()
        message = {
            'event': 'MODE_CHANGED',
            'payload': {
                'mode': 'DISABLED'
            }
        }
        layer._handle_custom_msg(message, None)
        assert layer.mode == 'DISABLED'

    def test_marker_options_change(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.observe(observer)
        new_options = marker.MarkerOptions(label='X')
        layer.marker_options = new_options
        assert layer.marker_options.label == 'X'
        assert len(observer.calls) == 1
        [call] = observer.calls
        assert call['new'] == new_options

    def test_single_marker_options_change(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.observe(observer)
        layer.marker_options.label = 'X'
        assert layer.marker_options.label == 'X'
        assert len(observer.calls) == 1
        [call] = observer.calls
        assert call['new'].label == 'X'
        assert call['name'] == 'marker_options'
