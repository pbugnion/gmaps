
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


def new_marker_message(latitude, longitude):
    message = {
        'event': 'OVERLAY_ADDED',
        'payload': {
            'overlayType': 'MARKER',
            'latitude': latitude,
            'longitude': longitude
        }
    }
    return message


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
        message = new_marker_message(latitude=25.0, longitude=-5.0)
        layer._handle_custom_msg(message, None)
        assert len(layer.overlays) == 1
        [new_marker] = layer.overlays
        assert new_marker.location == (25.0, -5.0)

    def test_adding_new_marker_callback(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.on_new_marker(observer)
        message = new_marker_message(latitude=25.0, longitude=-5.0)
        layer._handle_custom_msg(message, None)
        assert len(observer.calls) == 1
        [call] = observer.calls
        assert call.location == (25.0, -5.0)

    def test_adding_new_markers_via_overlays_callback(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.on_new_marker(observer)
        layer.overlays = [
            marker.Marker(location=(25.0, -5.0)),
            marker.Marker(location=(10.0, 30.0))
        ]
        assert len(observer.calls) == 2
        [call1, call2] = observer.calls
        assert call1.location == (25.0, -5.0)
        assert call2.location == (10.0, 30.0)

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
