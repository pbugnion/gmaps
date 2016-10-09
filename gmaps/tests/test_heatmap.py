
import unittest

from ..heatmap import _heatmap_options, _HeatmapOptionsMixin


class HeatmapLayer(unittest.TestCase):

    def setUp(self):
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]
        self.weights = [0.2, 0.5]
        self.merged_weight_locations = [
            (-5.0, 5.0, 0.2),
            (10.0, 10.0, 0.5)
        ]

    def _options_from_default(self, **options_override):
        default_options = {
            "weights": None,
            "max_intensity": None,
            "dissipating": True,
            "point_radius": None,
            "opacity": 0.6,
            "gradient": None
        }
        default_options.update(options_override)
        return default_options

    def test_weighted(self):
        options = self._options_from_default(weights=self.weights)
        heatmap_args, is_weighted = _heatmap_options(
            self.locations, **options)
        assert is_weighted
        assert heatmap_args["data"] == self.merged_weight_locations

    def test_weighted_numpy_array(self):
        import numpy as np
        locations = np.array(self.locations)
        weights = np.array(self.weights)
        options = self._options_from_default(weights=weights)
        heatmap_args, is_weighted = _heatmap_options(locations, **options)
        assert is_weighted
        assert heatmap_args["data"] == self.merged_weight_locations

    def test_not_weighted_numpy_array(self):
        import numpy as np
        locations = np.array(self.locations)
        options = self._options_from_default()
        heatmap_args, is_weighted = _heatmap_options(locations, **options)
        assert not is_weighted
        assert heatmap_args["data"] == self.locations


class TestHeatmapOptionsMixin(unittest.TestCase):

    def test_gradient_default_none(self):
        l = _HeatmapOptionsMixin()
        assert l.gradient is None

    def test_gradient_default_values(self):
        l = _HeatmapOptionsMixin(gradient=["blue", "red"])
        assert l.gradient == ["blue", "red"]

    def test_gradient_set_none(self):
        l = _HeatmapOptionsMixin(gradient=["blue", "red"])
        l.gradient = None
        assert l.gradient is None
