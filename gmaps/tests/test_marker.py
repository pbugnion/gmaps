
import unittest
import pytest

import numpy as np
import traitlets

from ..marker import (
    MarkerOptions,
    Marker,
    Markers,
    Symbol,
    marker_layer,
    symbol_layer
)


class MarkerLayer(unittest.TestCase):

    def setUp(self):
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]
        self.kwargs = {
            "hover_text": "",
            "label": "",
            "info_box_content": None,
            "display_info_box": None
        }

    def _add_default_options(self, **options):
        new_options = self.kwargs.copy()
        new_options.update(options)
        return new_options

    def test_locations(self):
        markers = marker_layer(self.locations)
        locations = [marker.location for marker in markers.markers]
        assert locations == self.locations

    def test_hover_text_atomic(self):
        options = self._add_default_options(hover_text="test-text")
        markers = marker_layer(self.locations, **options)
        for marker in markers.markers:
            assert marker.hover_text == "test-text"

    def test_hover_text_lists(self):
        options = self._add_default_options(hover_text=["t1", "t2"])
        markers = marker_layer(self.locations, **options)
        hover_texts = [marker.hover_text for marker in markers.markers]
        assert hover_texts == ["t1", "t2"]

    def test_infobox_content_atomic(self):
        test_content = "<h3>test-html-infobox</h3>"
        options = self._add_default_options(
            info_box_content=test_content, display_info_box=True)
        markers = marker_layer(self.locations, **options)
        for marker in markers.markers:
            assert marker.info_box_content == test_content
            assert marker.display_info_box

    def test_infobox_content_lists(self):
        test_content = ["<h1>h1</h1>", "<h2>h2</h2>"]
        test_display_info_box = [True, False]
        options = self._add_default_options(
            info_box_content=test_content,
            display_info_box=test_display_info_box)
        markers = marker_layer(self.locations, **options)
        info_contents = [marker.info_box_content for marker in markers.markers]
        display_infos = [marker.display_info_box for marker in markers.markers]
        assert tuple(info_contents) == tuple(test_content)
        assert tuple(display_infos) == tuple(test_display_info_box)

    def test_infobox_default_display(self):
        test_content = "test-content"
        options = self._add_default_options(info_box_content=test_content)
        markers = marker_layer(self.locations, **options)
        for marker in markers.markers:
            assert marker.info_box_content == "test-content"
            assert marker.display_info_box

    def test_infobox_default_display_lists(self):
        test_content = ["1", None]
        options = self._add_default_options(info_box_content=test_content)
        markers = marker_layer(self.locations, **options)
        display_infos = [marker.display_info_box for marker in markers.markers]
        assert tuple(display_infos) == (True, False)

    def test_locations_array(self):
        locations_array = np.array(self.locations)
        options = self._add_default_options()
        markers = marker_layer(locations_array, **options)
        locations = [marker.location for marker in markers.markers]
        assert locations == self.locations

    def test_locations_pandas_df(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame.from_records(
            self.locations, columns=["latitude", "longitude"])
        options = self._add_default_options()
        markers = marker_layer(df, **options)
        locations = [marker.location for marker in markers.markers]
        assert locations == self.locations

    def test_all_pandas_df(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame.from_records(
            [
                list(self.locations[0]) + ["text1", "a"],
                list(self.locations[1]) + ["text2", "b"],
            ],
            columns=["latitude", "longitude", "hover_text", "label"])
        options = self._add_default_options(
            hover_text=df["hover_text"], label=df["label"])
        markers = marker_layer(
            df[["latitude", "longitude"]], **options)
        locations = [marker.location for marker in markers.markers]
        assert locations == self.locations
        hover_texts = [marker.hover_text for marker in markers.markers]
        assert hover_texts == ["text1", "text2"]
        labels = [marker.label for marker in markers.markers]
        assert labels == ["a", "b"]


class SymbolLayer(unittest.TestCase):

    def setUp(self):
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]
        self.kwargs = {
            "stroke_color": None,
            "hover_text": "",
            "fill_color": "red",
            "scale": 5,
            "fill_opacity": 1.0,
            "stroke_opacity": 1.0,
            "info_box_content": None,
            "display_info_box": None
        }

    def _add_default_options(self, **options):
        new_options = self.kwargs.copy()
        new_options.update(options)
        return new_options

    def test_locations(self):
        symbols = symbol_layer(self.locations)
        locations = [symbol.location for symbol in symbols.markers]
        assert locations == self.locations

    def test_empty_locations(self):
        symbols = symbol_layer([])
        assert symbols.markers == []

    def test_stroke_color_atomic_text(self):
        options = self._add_default_options(stroke_color="red")
        symbols = symbol_layer(self.locations, **options)
        for symbol in symbols.markers:
            assert symbol.stroke_color == "red"

    def test_empty_locations_stroke_color(self):
        symbols = symbol_layer([], stroke_color="red")
        assert symbols.markers == []

    def test_stroke_color_atomic_tuple(self):
        color = (10, 10, 10, 0.5)
        options = self._add_default_options(stroke_color=color)
        symbols = symbol_layer(self.locations, **options)
        for symbol in symbols.markers:
            assert symbol.stroke_color == 'rgba(10,10,10,0.5)'

    def test_stroke_color_list_text(self):
        options = self._add_default_options(stroke_color=["red", "green"])
        symbols = symbol_layer(self.locations, **options)
        colors = [symbol.stroke_color for symbol in symbols.markers]
        assert colors == ["red", "green"]

    def test_stroke_color_list_tuples(self):
        c1 = (10, 10, 10, 0.5)
        c2 = (20, 20, 20, 0.5)
        options = self._add_default_options(stroke_color=[c1, c2])
        symbols = symbol_layer(self.locations, **options)
        colors = [symbol.stroke_color for symbol in symbols.markers]
        assert colors == ['rgba(10,10,10,0.5)', 'rgba(20,20,20,0.5)']

    def test_infobox_default(self):
        options = self._add_default_options()
        symbols = symbol_layer(self.locations, **options)
        for symbol in symbols.markers:
            assert not symbol.display_info_box

    def test_infobox_content_atomic(self):
        test_content = "<h3>test-html-infobox</h3>"
        options = self._add_default_options(
            info_box_content=test_content, display_info_box=True)
        symbols = symbol_layer(self.locations, **options)
        for symbol in symbols.markers:
            assert symbol.info_box_content == test_content
            assert symbol.display_info_box

    def test_infobox_content_lists(self):
        test_content = ["1", "2"]
        options = self._add_default_options(
            info_box_content=test_content, display_info_box=True)
        symbols = symbol_layer(self.locations, **options)
        content_options = [
            symbol.info_box_content for symbol in symbols.markers
        ]
        assert content_options == test_content

    def test_infobox_default_display_lists(self):
        test_content = ["1", None]
        options = self._add_default_options(info_box_content=test_content)
        symbols = symbol_layer(self.locations, **options)
        display_infos = [symbol.display_info_box for symbol in symbols.markers]
        assert display_infos == [True, False]

    def test_opacity_default(self):
        options = self._add_default_options()
        symbols = symbol_layer(self.locations, **options)
        for symbol in symbols.markers:
            assert symbol.fill_opacity == 1.0
            assert symbol.stroke_opacity == 1.0

    def test_opacity_single(self):
        options = self._add_default_options(
            fill_opacity=0.2, stroke_opacity=0.5)
        symbols = symbol_layer(self.locations, **options)
        for symbol in symbols.markers:
            assert symbol.fill_opacity == 0.2
            assert symbol.stroke_opacity == 0.5

    def test_opacity_list(self):
        options = self._add_default_options(
            fill_opacity=[0.2, 0.4], stroke_opacity=[0.6, 0.7])
        symbols = symbol_layer(self.locations, **options)
        fill_opacity_options = [
            symbol.fill_opacity for symbol in symbols.markers
        ]
        stroke_opacity_options = [
            symbol.stroke_opacity for symbol in symbols.markers
        ]
        assert fill_opacity_options == [0.2, 0.4]
        assert stroke_opacity_options == [0.6, 0.7]


class MarkerOptionsTests(unittest.TestCase):

    def test_defaults(self):
        options = MarkerOptions()
        assert options.hover_text == ''
        assert not options.display_info_box
        assert options.info_box_content == ''
        assert options.label == ''

    def test_hover_text(self):
        options = MarkerOptions(hover_text='some text')
        assert options.hover_text == 'some text'

    def test_label(self):
        options = MarkerOptions(label='C')
        assert options.label == 'C'

    def test_with_info_box(self):
        options = MarkerOptions(info_box_content='some text')
        assert options.display_info_box
        assert options.info_box_content == 'some text'

    def test_no_info_box(self):
        options = MarkerOptions(
            info_box_content='some text',
            display_info_box=False)
        assert not options.display_info_box
        assert options.info_box_content == 'some text'


class MarkerTest(unittest.TestCase):

    def test_location_kwargs(self):
        marker = Marker(location=(10.0, 5.0))
        assert marker.get_state()['location'] == (10.0, 5.0)

    def test_location_non_kwarg(self):
        marker = Marker((10.0, 5.0))
        assert marker.get_state()['location'] == (10.0, 5.0)

    def test_with_info_box(self):
        marker = Marker((10.0, 5.0), info_box_content='test-content')
        assert marker.display_info_box
        assert marker.info_box_content == 'test-content'

    def test_no_info_box(self):
        marker = Marker(location=(10.0, 5.0))
        assert not marker.display_info_box

    def test_explicit_hide_info_box(self):
        marker = Marker(
            (10.0, 5.0),
            display_info_box=False,
            info_box_content='test-content'
        )
        assert not marker.display_info_box
        assert marker.info_box_content == 'test-content'


class SymbolTest(unittest.TestCase):

    def setUp(self):
        self.location = (10.0, 5.0)

    def test_defaults(self):
        symbol = Symbol(self.location)
        state = symbol.get_state()
        assert state['fill_color'] is None
        assert state['fill_opacity'] == 1.0
        assert state['stroke_color'] is None
        assert state['stroke_opacity'] == 1.0
        assert state['scale'] == 4

    def test_set_fill_opacity(self):
        symbol = Symbol(self.location, fill_opacity=0.2)
        assert symbol.get_state()['fill_opacity'] == 0.2
        symbol.fill_opacity = 0.8
        assert symbol.get_state()['fill_opacity'] == 0.8

    def test_invalid_fill_opacity(self):
        with self.assertRaises(traitlets.TraitError):
            Symbol(self.location, fill_opacity=-0.2)
        with self.assertRaises(traitlets.TraitError):
            Symbol(self.location, fill_opacity=1.2)
        with self.assertRaises(traitlets.TraitError):
            Symbol(self.location, fill_opacity='not-a-float')

    def test_set_stroke_opacity(self):
        symbol = Symbol(self.location, stroke_opacity=0.2)
        assert symbol.get_state()['stroke_opacity'] == 0.2
        symbol.stroke_opacity = 0.8
        assert symbol.get_state()['stroke_opacity'] == 0.8

    def test_invalid_stroke_opacity(self):
        with self.assertRaises(traitlets.TraitError):
            Symbol(self.location, stroke_opacity=-0.2)
        with self.assertRaises(traitlets.TraitError):
            Symbol(self.location, stroke_opacity=1.2)
        with self.assertRaises(traitlets.TraitError):
            Symbol(self.location, stroke_opacity='not-a-float')


class MarkersTest(unittest.TestCase):

    def setUp(self):
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]
        self.symbols = [
            Symbol(location=location)
            for location in self.locations
        ]

    def test_bounds_markers(self):
        layer = Markers(markers=self.symbols)
        assert layer.has_bounds
        assert layer.data_bounds

    def test_bounds_no_markers(self):
        layer = Markers(markers=[])
        assert not layer.has_bounds
