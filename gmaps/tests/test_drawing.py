
import unittest

import traitlets

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
        'event': 'FEATURE_ADDED',
        'payload': {
            'featureType': 'MARKER',
            'latitude': latitude,
            'longitude': longitude
        }
    }
    return message


def new_line_message(start, end):
    message = {
        'event': 'FEATURE_ADDED',
        'payload': {
            'featureType': 'LINE',
            'start': start,
            'end': end
        }
    }
    return message


def new_polygon_message(path):
    message = {
        'event': 'FEATURE_ADDED',
        'payload': {
            'featureType': 'POLYGON',
            'path': path
        }
    }
    return message


class Drawing(unittest.TestCase):

    def test_default_features(self):
        layer = drawing.Drawing()
        assert layer.get_state()['features'] == []

    def test_with_features(self):
        marker_widget = marker.Marker((5.0, 10.0))
        layer = drawing.Drawing(features=[marker_widget])
        features = layer.get_state()['features']
        assert len(features) == 1
        [serialized_marker] = features
        expected = 'IPY_MODEL_{}'.format(marker_widget.model_id)
        assert serialized_marker == expected

    def test_adding_marker(self):
        layer = drawing.Drawing()
        message = new_marker_message(latitude=25.0, longitude=-5.0)
        layer._handle_custom_msg(message, None)
        assert len(layer.features) == 1
        [new_marker] = layer.features
        assert new_marker.location == (25.0, -5.0)

    def test_adding_new_marker_callback(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.on_new_feature(observer)
        message = new_marker_message(latitude=25.0, longitude=-5.0)
        layer._handle_custom_msg(message, None)
        assert len(observer.calls) == 1
        [call] = observer.calls
        assert call.location == (25.0, -5.0)

    def test_adding_new_markers_via_overlays_callback(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.on_new_feature(observer)
        layer.features = [
            marker.Marker(location=(25.0, -5.0)),
            marker.Marker(location=(10.0, 30.0))
        ]
        assert len(observer.calls) == 2
        [call1, call2] = observer.calls
        assert call1.location == (25.0, -5.0)
        assert call2.location == (10.0, 30.0)

    def test_adding_line(self):
        layer = drawing.Drawing()
        message = new_line_message(start=(5.0, 10.0), end=(-5.0, -2.0))
        layer._handle_custom_msg(message, None)
        assert len(layer.features) == 1
        [new_line] = layer.features
        assert new_line.start == (5.0, 10.0)
        assert new_line.end == (-5.0, -2.0)

    def test_adding_line_callback(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.on_new_feature(observer)
        message = new_line_message(start=(5.0, 10.0), end=(-5.0, -2.0))
        layer._handle_custom_msg(message, None)
        assert len(observer.calls) == 1
        [call] = observer.calls
        assert call.start == (5.0, 10.0)
        assert call.end == (-5.0, -2.0)

    def test_adding_line_features(self):
        observer = UnaryFunctionMock()
        layer = drawing.Drawing()
        layer.on_new_feature(observer)
        layer.features = [
            drawing.Line(start=(5.0, 10.0), end=(-5.0, -2.0))
        ]
        assert len(observer.calls) == 1
        [call] = observer.calls
        assert call.start == (5.0, 10.0)
        assert call.end == (-5.0, -2.0)

    def test_adding_polygon(self):
        layer = drawing.Drawing()
        path = [(5.0, 10.0), (15.0, 20.0), (25.0, 50.0)]
        message = new_polygon_message(path)
        layer._handle_custom_msg(message, None)
        assert len(layer.features) == 1
        [new_polygon] = layer.features
        assert new_polygon.path == path

    def test_default_mode(self):
        layer = drawing.Drawing()
        assert layer.get_state()['mode'] == drawing.DEFAULT_DRAWING_MODE

    def test_default_mode_hide_controls(self):
        controls = drawing.DrawingControls(show_controls=False)
        layer = drawing.Drawing(toolbar_controls=controls)
        assert layer.get_state()['mode'] == 'DISABLED'

    def test_changing_mode(self):
        layer = drawing.Drawing(mode='LINE')
        assert layer.get_state()['mode'] == 'LINE'

    def test_receiving_mode_changes(self):
        layer = drawing.Drawing()
        message = {
            'event': 'MODE_CHANGED',
            'payload': {
                'mode': 'LINE'
            }
        }
        layer._handle_custom_msg(message, None)
        assert layer.mode == 'LINE'

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


class DrawingFactory(unittest.TestCase):

    def test_defaults(self):
        layer = drawing.drawing_layer()
        assert layer.toolbar_controls.show_controls
        assert layer.mode == drawing.DEFAULT_DRAWING_MODE
        assert layer.features == []

    def test_hide_controls(self):
        layer = drawing.drawing_layer(show_controls=False)
        assert not layer.toolbar_controls.show_controls

    def test_different_mode(self):
        layer = drawing.drawing_layer(mode='DISABLED')
        assert layer.mode == 'DISABLED'

    def test_with_overlays(self):
        new_marker = marker.Marker(location=(-25.0, 5.0))
        layer = drawing.drawing_layer(features=[new_marker])
        assert layer.features == [new_marker]

    def test_accept_marker_options(self):
        layer = drawing.drawing_layer(
            marker_options=marker.MarkerOptions(label='B'))
        assert layer.marker_options.label == 'B'

    def test_accept_marker_options_dict(self):
        layer = drawing.drawing_layer(
            marker_options={'label': 'B'})
        assert layer.marker_options.label == 'B'

    def test_accept_marker_options_info_box(self):
        layer = drawing.drawing_layer(
            marker_options={'info_box_content': 'hello world'})
        assert layer.marker_options.info_box_content == 'hello world'
        assert layer.marker_options.display_info_box


class Line(unittest.TestCase):

    def test_start_end_kwargs(self):
        line = drawing.Line(
            start=(5.0, 10.0),
            end=(20.0, 30.0)
        )
        assert line.get_state()['start'] == (5.0, 10.0)
        assert line.get_state()['end'] == (20.0, 30.0)

    def test_missing_start(self):
        with self.assertRaises(TypeError):
            drawing.Line(end=(20.0, 30.0))

    def test_missing_end(self):
        with self.assertRaises(TypeError):
            drawing.Line(start=(20.0, 30.0))

    def test_normal_arguments(self):
        line = drawing.Line((5.0, 10.0), (20.0, 30.0))
        assert line.get_state()['start'] == (5.0, 10.0)
        assert line.get_state()['end'] == (20.0, 30.0)


class Polygon(unittest.TestCase):

    def test_path_kwarg(self):
        path = [(10.0, 20.0), (5.0, 30.0), (-5.0, 10.0)]
        polygon = drawing.Polygon(path=path)
        assert polygon.get_state()['path'] == path

    def test_normal_path_arg(self):
        path = [(10.0, 20.0), (5.0, 30.0), (-5.0, 10.0)]
        polygon = drawing.Polygon(path)
        assert polygon.get_state()['path'] == path

    def test_missing_path(self):
        with self.assertRaises(TypeError):
            drawing.Polygon()

    def test_insufficient_points_path(self):
        with self.assertRaises(traitlets.TraitError):
            path = [(5.0, 30.0), (-5.0, 10.0)]
            drawing.Polygon(path)
