
import ipywidgets as widgets

from traitlets import Unicode, Instance

from .maps import Map, InitialViewport
from .toolbar import Toolbar
from .errors_box import ErrorsBox

__all__ = ["Figure", "figure"]


class Figure(widgets.DOMWidget):
    """
    Figure widget

    This is the base widget for a Figure. Prefer instantiating
    instances of ``Figure`` using the :func:`gmaps.figure`
    factory method.
    """
    _view_name = Unicode("FigureView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("FigureModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    _toolbar = Instance(Toolbar, allow_none=True, default=None).tag(
        sync=True, **widgets.widget_serialization)
    _errors_box = Instance(ErrorsBox, allow_none=True, default=None).tag(
        sync=True, **widgets.widget_serialization)
    _map = Instance(Map).tag(sync=True, **widgets.widget_serialization)

    def add_layer(self, layer):
        """
        Add a data layer to this figure.

        :param layer: a `gmaps` layer.

        :Examples:

        >>> f = figure()
        >>> fig.add_layer(gmaps.heatmap_layer(locations))

        .. seealso:: layer creation functions

            :func:`gmaps.heatmap_layer`
                Create a heatmap layer

            :func:`gmaps.symbol_layer`
                Create a layer of symbols

            :func:`gmaps.marker_layer`
                Create a layer of markers

            :func:`gmaps.geojson_layer`
                Create a GeoJSON layer

            :func:`gmaps.directions_layer`
                Create a layer with directions
        """
        self._map.add_layer(layer)


def figure(
        display_toolbar=True, display_errors=True, zoom_level=None,
        map_center=None):
    """
    Create a gmaps figure

    This returns a `Figure` object to which you can add data layers.

    :param display_toolbar:
        Boolean denoting whether to show the toolbar. Defaults to True.

    :param display_errors:
        Boolean denoting whether to show errors that arise in the client.
        Defaults to True.

    :returns:
        A :class:`gmaps.Figure` widget.

    :Examples:

    >>> import gmaps
    >>> gmaps.configure(api_key="AI...")
    >>> fig = gmaps.figure()
    >>> fig.add_layer(gmaps.heatmap_layer(locations))
    """
    if zoom_level is not None or map_center is not None:
        if zoom_level is None or map_center is None:
            raise ValueError(
                "Either both zoom_level and map_center "
                "should be specified, or neither"
            )
        else:
            initial_viewport = InitialViewport.from_zoom_center(
                    zoom_level, map_center)
    else:
        initial_viewport = InitialViewport.from_data_bounds()
    _map = Map(initial_viewport=initial_viewport)
    _toolbar = Toolbar() if display_toolbar else None
    _errors_box = ErrorsBox() if display_errors else None
    return Figure(_map=_map, _toolbar=_toolbar, _errors_box=_errors_box)
