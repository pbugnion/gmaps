
import ipywidgets as widgets
from traitlets import (Unicode, default, List, Tuple, Instance,
                       observe, Dict, HasTraits)

DEFAULT_CENTER = (46.2, 6.1)
DEFAULT_BOUNDS = [(46.2, 6.1), (47.2, 7.1)]

_default_configuration = {"api_key": None}


def configure(api_key=None):
    """
    Configure access to the GoogleMaps API.

    :param api_key: String denoting the key to use when accessing Google maps,
        or None to not pass an API key.
    """
    configuration = {"api_key": api_key}
    global _default_configuration
    _default_configuration = configuration


class ConfigurationMixin(HasTraits):
    configuration = Dict(
        traits={"api_key": Unicode(allow_none=True)}).tag(sync=True)

    @default("configuration")
    def _config_default(self):
        return _default_configuration


class Map(widgets.DOMWidget, ConfigurationMixin):
    """
    Base map class

    Instances of this act as a base map on which you can add
    additional layers.

    :Examples:

    >>> m = gmaps.Map()
    >>> m.add_layer(gmaps.heatmap_layer(locations))
    """
    _view_name = Unicode("PlainmapView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("PlainmapModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    layers = Tuple(trait=Instance(widgets.Widget)).tag(
        sync=True, **widgets.widget_serialization)
    data_bounds = List(DEFAULT_BOUNDS).tag(sync=True)

    def add_layer(self, layer):
        self.layers = tuple([l for l in self.layers] + [layer])

    @default("layout")
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    @observe("layers")
    def _calc_bounds(self, change):
        layers = change["new"]
        bounds_list = [
            layer.data_bounds for layer in layers if layer.has_bounds
        ]
        if bounds_list:
            min_latitude = min(bounds[0][0] for bounds in bounds_list)
            min_longitude = min(bounds[0][1] for bounds in bounds_list)
            max_latitude = min(bounds[1][0] for bounds in bounds_list)
            max_longitude = min(bounds[1][1] for bounds in bounds_list)
            self.data_bounds = [
                (min_latitude, min_longitude),
                (max_latitude, max_longitude)
            ]
