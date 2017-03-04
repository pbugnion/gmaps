
import unittest
import pytest

import numpy as np

from ..marker import _marker_layer_options, _symbol_layer_options


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

    def test_hover_text_atomic(self):
        options = self._add_default_options(hover_text="test-text")
        marker_options = _marker_layer_options(self.locations, **options)
        for options in marker_options:
            assert options["hover_text"] == "test-text"

    def test_hover_text_lists(self):
        options = self._add_default_options(hover_text=["t1", "t2"])
        marker_options = _marker_layer_options(self.locations, **options)
        hover_texts = [opts["hover_text"] for opts in marker_options]
        assert tuple(hover_texts) == ("t1", "t2")

    def test_infobox_content_atomic(self):
        test_content = "<h3>test-html-infobox</h3>"
        options = self._add_default_options(
            info_box_content=test_content, display_info_box=True)
        marker_options = _marker_layer_options(self.locations, **options)
        for options in marker_options:
            assert options["info_box_content"] == test_content
            assert options["display_info_box"]

    def test_infobox_content_lists(self):
        test_content = ["<h1>h1</h1>", "<h2>h2</h2>"]
        test_display_info_box = [True, False]
        options = self._add_default_options(
            info_box_content=test_content,
            display_info_box=test_display_info_box)
        marker_options = _marker_layer_options(self.locations, **options)
        info_contents = [opts["info_box_content"] for opts in marker_options]
        display_infos = [opts["display_info_box"] for opts in marker_options]
        assert tuple(info_contents) == tuple(test_content)
        assert tuple(display_infos) == tuple(test_display_info_box)

    def test_infobox_default_display(self):
        test_content = "test-content"
        options = self._add_default_options(info_box_content=test_content)
        marker_options = _marker_layer_options(self.locations, **options)
        for options in marker_options:
            assert options["display_info_box"]

    def test_infobox_default_display_lists(self):
        test_content = ["1", None]
        options = self._add_default_options(info_box_content=test_content)
        marker_options = _marker_layer_options(self.locations, **options)
        display_infos = [opts["display_info_box"] for opts in marker_options]
        assert tuple(display_infos) == (True, False)

    def test_locations_array(self):
        locations_array = np.array(self.locations)
        options = self._add_default_options()
        marker_options = _marker_layer_options(locations_array, **options)
        locations = [opts["location"] for opts in marker_options]
        assert locations == self.locations

    def test_locations_pandas_df(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame.from_records(
            self.locations, columns=["latitude", "longitude"])
        options = self._add_default_options()
        marker_options = _marker_layer_options(df, **options)
        locations = [opts["location"] for opts in marker_options]
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
        marker_options = _marker_layer_options(
            df[["latitude", "longitude"]], **options)
        locations = [opts["location"] for opts in marker_options]
        assert locations == self.locations
        hover_texts = [opts["hover_text"] for opts in marker_options]
        assert hover_texts == ["text1", "text2"]
        labels = [opts["label"] for opts in marker_options]
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

    def test_stroke_color_atomic_text(self):
        options = self._add_default_options(stroke_color="red")
        symbol_options = _symbol_layer_options(
            self.locations, **options)
        for options in symbol_options:
            assert options["stroke_color"] == "red"

    def test_stroke_color_atomic_tuple(self):
        color = (10, 10, 10, 0.5)
        options = self._add_default_options(stroke_color=color)
        symbol_options = _symbol_layer_options(self.locations, **options)
        for options in symbol_options:
            assert options["stroke_color"] == color

    def test_stroke_color_list_text(self):
        options = self._add_default_options(stroke_color=["red", "green"])
        symbol_options = _symbol_layer_options(self.locations, **options)
        opts = [opts["stroke_color"] for opts in symbol_options]
        assert tuple(opts) == ("red", "green")

    def test_stroke_color_list_tuples(self):
        c1 = (10, 10, 10, 0.5)
        c2 = (20, 20, 20, 0.5)
        options = self._add_default_options(stroke_color=[c1, c2])
        symbol_options = _symbol_layer_options(self.locations, **options)
        colors = [opts["stroke_color"] for opts in symbol_options]
        assert tuple(colors) == (c1, c2)

    def test_infobox_default(self):
        options = self._add_default_options()
        symbol_options = _symbol_layer_options(self.locations, **options)
        for opts in symbol_options:
            assert not opts["display_info_box"]

    def test_infobox_content_atomic(self):
        test_content = "<h3>test-html-infobox</h3>"
        options = self._add_default_options(
            info_box_content=test_content, display_info_box=True)
        symbol_options = _symbol_layer_options(self.locations, **options)
        for options in symbol_options:
            assert options["info_box_content"] == test_content
            assert options["display_info_box"]

    def test_infobox_content_lists(self):
        test_content = ["1", "2"]
        options = self._add_default_options(
            info_box_content=test_content, display_info_box=True)
        symbol_options = _symbol_layer_options(self.locations, **options)
        content_options = [opts["info_box_content"] for opts in symbol_options]
        assert tuple(content_options) == tuple(test_content)

    def test_infobox_default_display_lists(self):
        test_content = ["1", None]
        options = self._add_default_options(info_box_content=test_content)
        marker_options = _symbol_layer_options(self.locations, **options)
        display_infos = [opts["display_info_box"] for opts in marker_options]
        assert tuple(display_infos) == (True, False)
