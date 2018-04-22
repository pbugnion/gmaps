
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

    def test_marker_options_instance(self):
        options = marker.MarkerOptions(label='C')
        layer = drawing.Drawing(marker_options=options)
        assert layer.marker_options.label == 'C'

    def test_marker_options_dict(self):
        options = {'label': 'C'}
        layer = drawing.Drawing(marker_options=options)
        assert layer.marker_options.label == 'C'

    def test_accept_marker_options_info_box(self):
        layer = drawing.Drawing(
            marker_options={'info_box_content': 'hello world'})
        assert layer.marker_options.info_box_content == 'hello world'
        assert layer.marker_options.display_info_box

    def test_line_options_instance(self):
        options = drawing.LineOptions(stroke_weight=12.0)
        layer = drawing.Drawing(line_options=options)
        assert layer.line_options.stroke_weight == 12.0

    def test_line_options_dict(self):
        options = {'stroke_weight': 12.0}
        layer = drawing.Drawing(line_options=options)
        assert layer.line_options.stroke_weight == 12.0

    def test_polygon_options_instance(self):
        options = drawing.PolygonOptions(stroke_weight=12.0)
        layer = drawing.Drawing(polygon_options=options)
        assert layer.polygon_options.stroke_weight == 12.0

    def test_polygon_options_dict(self):
        options = {'stroke_weight': 12.0}
        layer = drawing.Drawing(polygon_options=options)
        assert layer.polygon_options.stroke_weight == 12.0

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

    def test_adding_marker_with_marker_options(self):
        layer = drawing.Drawing(marker_options=marker.MarkerOptions(label='C'))
        message = new_marker_message(latitude=25.0, longitude=-5.0)
        layer._handle_custom_msg(message, None)
        assert len(layer.features) == 1
        [new_marker] = layer.features
        assert new_marker.label == 'C'

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

    def test_adding_line_with_line_options(self):
        layer = drawing.Drawing(
            line_options=drawing.LineOptions(stroke_weight=19.0))
        message = new_line_message(start=(5.0, 10.0), end=(-5.0, -2.0))
        layer._handle_custom_msg(message, None)
        assert len(layer.features) == 1
        [new_line] = layer.features
        assert new_line.start == (5.0, 10.0)
        assert new_line.end == (-5.0, -2.0)
        assert new_line.stroke_weight == 19.0

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

    def test_adding_polygon_with_options(self):
        layer = drawing.Drawing(
            polygon_options=drawing.PolygonOptions(stroke_weight=19.0))
        path = [(5.0, 10.0), (15.0, 20.0), (25.0, 50.0)]
        message = new_polygon_message(path)
        layer._handle_custom_msg(message, None)
        assert len(layer.features) == 1
        [new_polygon] = layer.features
        assert new_polygon.path == path
        assert new_polygon.stroke_weight == 19.0

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

    def test_with_features(self):
        new_marker = marker.Marker(location=(-25.0, 5.0))
        layer = drawing.drawing_layer(features=[new_marker])
        assert layer.features == [new_marker]

    def test_with_polygon_options(self):
        layer = drawing.drawing_layer(polygon_options={'stroke_weight': 12.0})
        assert layer.polygon_options.stroke_weight == 12.0


class Line(unittest.TestCase):

    def setUp(self):
        self.start = (5.0, 10.0)
        self.end = (20.0, 30.0)

    def test_start_end_kwargs(self):
        line = drawing.Line(
            start=self.start,
            end=self.end
        )
        assert line.get_state()['start'] == self.start
        assert line.get_state()['end'] == self.end

    def test_missing_start(self):
        with self.assertRaises(TypeError):
            drawing.Line(end=(20.0, 30.0))

    def test_missing_end(self):
        with self.assertRaises(TypeError):
            drawing.Line(start=(20.0, 30.0))

    def test_normal_arguments(self):
        line = drawing.Line(self.start, self.end)
        assert line.get_state()['start'] == self.start
        assert line.get_state()['end'] == self.end

    def test_defaults(self):
        line = drawing.Line(self.start, self.end)
        assert line.get_state()['stroke_opacity'] == 0.6

    def test_set_opacity(self):
        line = drawing.Line(self.start, self.end, stroke_opacity=0.2)
        assert line.get_state()['stroke_opacity'] == 0.2

    def test_invalid_opacity(self):
        with self.assertRaises(traitlets.TraitError):
            drawing.Line(self.start, self.end, stroke_opacity=-0.2)
        with self.assertRaises(traitlets.TraitError):
            drawing.Line(self.start, self.end, stroke_opacity=1.2)
        with self.assertRaises(traitlets.TraitError):
            drawing.Line(self.start, self.end, stroke_opacity='not-a-float')


class Polygon(unittest.TestCase):

    def setUp(self):
        self.path = [(10.0, 20.0), (5.0, 30.0), (-5.0, 10.0)]

    def test_path_kwarg(self):
        polygon = drawing.Polygon(path=self.path)
        assert polygon.get_state()['path'] == self.path

    def test_normal_path_arg(self):
        polygon = drawing.Polygon(self.path)
        assert polygon.get_state()['path'] == self.path

    def test_missing_path(self):
        with self.assertRaises(TypeError):
            drawing.Polygon()

    def test_insufficient_points_path(self):
        with self.assertRaises(traitlets.TraitError):
            path = [(5.0, 30.0), (-5.0, 10.0)]
            drawing.Polygon(path)

    def test_defaults(self):
        polygon = drawing.Polygon(self.path)
        state = polygon.get_state()
        assert state['stroke_color'] == drawing.DEFAULT_STROKE_COLOR
        assert state['stroke_weight'] == 2.0
        assert state['stroke_opacity'] == 0.6
        assert state['fill_color'] == drawing.DEFAULT_FILL_COLOR
        assert state['fill_opacity'] == 0.2

    def test_custom_arguments(self):
        polygon = drawing.Polygon(
            self.path,
            stroke_color=(1, 3, 5),
            stroke_weight=10.0,
            stroke_opacity=0.87,
            fill_color=(7, 9, 11),
            fill_opacity=0.76
        )
        state = polygon.get_state()
        assert state['stroke_color'] == 'rgb(1,3,5)'
        assert state['stroke_weight'] == 10.0
        assert state['stroke_opacity'] == 0.87
        assert state['fill_color'] == 'rgb(7,9,11)'
        assert state['fill_opacity'] == 0.76

    def test_invalid_stroke_opacity(self):
        with self.assertRaises(traitlets.TraitError):
            drawing.Polygon(self.path, stroke_opacity=-0.2)
        with self.assertRaises(traitlets.TraitError):
            drawing.Polygon(self.path, stroke_opacity=1.2)
        with self.assertRaises(traitlets.TraitError):
            drawing.Polygon(self.path, stroke_opacity='not-a-float')

    def test_invalid_fill_opacity(self):
        with self.assertRaises(traitlets.TraitError):
            drawing.Polygon(self.path, fill_opacity=-0.2)
        with self.assertRaises(traitlets.TraitError):
            drawing.Polygon(self.path, fill_opacity=1.2)
        with self.assertRaises(traitlets.TraitError):
            drawing.Polygon(self.path, fill_opacity='not-a-float')


class PolygonOptions(unittest.TestCase):

    def test_to_polygon_defaults(self):
        path = [(10.0, 20.0), (5.0, 30.0), (-5.0, 10.0)]
        expected_polygon = drawing.Polygon(path)
        actual_polygon = drawing.PolygonOptions().to_polygon(path)
        assert actual_polygon.path == expected_polygon.path
        assert actual_polygon.stroke_color == expected_polygon.stroke_color
        assert actual_polygon.stroke_weight == expected_polygon.stroke_weight
        assert actual_polygon.stroke_opacity == expected_polygon.stroke_opacity
        assert actual_polygon.fill_color == expected_polygon.fill_color
        assert actual_polygon.fill_opacity == expected_polygon.fill_opacity
