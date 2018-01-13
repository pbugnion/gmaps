
import unittest
import pytest

from ..heatmap import _heatmap_options, _HeatmapOptionsMixin, heatmap_layer


class HeatmapLayer(unittest.TestCase):

    def setUp(self):
        self.locations = [(-5.0, 5.0), (10.0, 10.0)]
        self.weights = [0.2, 0.5]

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
        heatmap = heatmap_layer(self.locations, weights=self.weights)
        state = heatmap.get_state()
        assert state['_view_name'] == 'WeightedHeatmapLayerView'
        assert state['_model_name'] == 'WeightedHeatmapLayerModel'
        assert state['weights'] == self.weights
        assert state['data'] == self.locations

    def test_weighted_numpy_array(self):
        import numpy as np
        locations = np.array(self.locations)
        weights = np.array(self.weights)
        heatmap = heatmap_layer(locations, weights=weights)
        state = heatmap.get_state()
        assert state['weights'] == self.weights
        assert state['data'] == self.locations

    def test_not_weighted_numpy_array(self):
        import numpy as np
        locations = np.array(self.locations)
        heatmap = heatmap_layer(locations)
        state = heatmap.get_state()
        assert state['_view_name'] == 'SimpleHeatmapLayerView'
        assert state['_model_name'] == 'SimpleHeatmapLayerModel'
        assert state['data'] == self.locations

    def test_weighted_pandas_df(self):
        pd = pytest.importorskip('pandas')
        df = pd.DataFrame.from_items([
            ('latitude', [loc[0] for loc in self.locations]),
            ('longitude', [loc[1] for loc in self.locations]),
            ('weight', self.weights)
        ])
        heatmap = heatmap_layer(
            df[['latitude', 'longitude']],
            weights=df['weight']
        )
        state = heatmap.get_state()
        assert state['_view_name'] == 'WeightedHeatmapLayerView'
        assert state['_model_name'] == 'WeightedHeatmapLayerModel'
        assert state['weights'] == self.weights
        assert state['data'] == self.locations

    def test_not_weighted_pandas_df(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame.from_items([
            ('latitude', [loc[0] for loc in self.locations]),
            ('longitude', [loc[1] for loc in self.locations]),
        ])
        heatmap = heatmap_layer(df[['latitude', 'longitude']])
        state = heatmap.get_state()
        assert state['_view_name'] == 'SimpleHeatmapLayerView'
        assert state['_model_name'] == 'SimpleHeatmapLayerModel'
        assert state['data'] == self.locations

    def test_max_intensity(self):
        heatmap = heatmap_layer(self.locations, max_intensity=0.2)
        state = heatmap.get_state()
        assert state['max_intensity'] == 0.2


class TestHeatmapOptionsMixin(unittest.TestCase):

    def test_gradient_default_none(self):
        layer = _HeatmapOptionsMixin()
        assert layer.gradient is None

    def test_gradient_default_values(self):
        layer = _HeatmapOptionsMixin(gradient=["blue", "red"])
        assert layer.gradient == ["blue", "red"]

    def test_gradient_set_none(self):
        layer = _HeatmapOptionsMixin(gradient=["blue", "red"])
        layer.gradient = None
        assert layer.gradient is None
