
import ipywidgets as widgets

from traitlets import Unicode, Instance, default, link

from .maps import (
    Map, InitialViewport, GMapsWidgetMixin, map_params_doc_snippets
)
from .geotraitlets import MapType, MouseHandling, Tilt
from .toolbar import Toolbar
from .errors_box import ErrorsBox
from ._docutils import doc_subst

__all__ = ["Figure", "figure"]


class FigureLayout(widgets.Layout):
    """
    Customised layout that returns a default height
    """

    @default('height')
    def _default_height(self):
        return '420px'


class Figure(GMapsWidgetMixin, widgets.DOMWidget):
    """
    Figure widget

    This is the base widget for a Figure. Prefer instantiating
    instances of ``Figure`` using the :func:`gmaps.figure`
    factory method.
    """
    _view_name = Unicode("FigureView").tag(sync=True)
    _model_name = Unicode("FigureModel").tag(sync=True)
    _toolbar = Instance(Toolbar, allow_none=True, default=None).tag(
        sync=True, **widgets.widget_serialization)
    _errors_box = Instance(ErrorsBox, allow_none=True, default=None).tag(
        sync=True, **widgets.widget_serialization)
    _map = Instance(Map).tag(sync=True, **widgets.widget_serialization)
    map_type = MapType('ROADMAP')
    tilt = Tilt()
    mouse_handling = MouseHandling('COOPERATIVE')
    layout = widgets.trait_types.InstanceDict(FigureLayout).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, *args, **kwargs):
        if kwargs.get('layout') is None:
            kwargs['layout'] = self._default_layout()
        super(Figure, self).__init__(*args, **kwargs)
        self._map.map_type = self.map_type
        link((self._map, 'map_type'), (self, 'map_type'))

        self._map.tilt = self.tilt
        link((self._map, 'tilt'), (self, 'tilt'))

        self._map.mouse_handling = self.mouse_handling
        link((self._map, 'mouse_handling'), (self, 'mouse_handling'))

    @default('layout')
    def _default_layout(self):
        return FigureLayout()

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

            :func:`gmaps.drawing_layer`
                Create a layer of custom features, and allow users to draw
                on the map

            :func:`gmaps.directions_layer`
                Create a layer with directions

            :func:`gmaps.bicycling_layer`
                Create a layer showing cycle routes

            :func:`gmaps.transit_layer`
                Create a layer showing public transport

            :func:`gmaps.traffic_layer`
                Create a layer showing current traffic information
        """
        try:
            toolbar_controls = layer.toolbar_controls
            if self._toolbar is not None and toolbar_controls is not None:
                self._toolbar.add_controls(toolbar_controls)
        except AttributeError:
            pass
        self._map.add_layer(layer)


@doc_subst(map_params_doc_snippets)
def figure(
        display_toolbar=True, display_errors=True, zoom_level=None, tilt=45,
        center=None, layout=None, map_type='ROADMAP',
        mouse_handling='COOPERATIVE'):
    """
    Create a gmaps figure

    This returns a `Figure` object to which you can add data layers.

    :param display_toolbar:
        Boolean denoting whether to show the toolbar. Defaults to True.
    :type display_toolbar: boolean, optional

    :param display_errors:
        Boolean denoting whether to show errors that arise in the client.
        Defaults to True.
    :type display_errors: boolean, optional

    :param zoom_level:
        Integer between 0 and 21 indicating the initial zoom level.
        High values are more zoomed in.
        By default, the zoom level is chosen to fit the data passed to the
        map. If specified, you must also specify the map center.
    :type zoom_level: int, optional

    :param tilt:
        Tilt can be either 0 or 45 indicating the tilt angle in
        degrees.  45-degree imagery is only available for satellite
        and hybrid map types, and is not available at every location
        at every zoom level. For locations where 45-degree imagery is
        not available, Google Maps will automatically fall back to 0
        tilt.
    :type tilt: int, optional

    :param center:
        Latitude-longitude pair determining the map center.
        By default, the map center is chosen to fit the data passed to the
        map. If specified, you must also specify the zoom level.
    :type center: tuple, optional

    {map_type}

    {mouse_handling}

    :param layout:
        Control the layout of the figure, e.g. its width, height, border etc.
        For instance, passing ``layout={{'width': '400px', 'height': '300px'}}``
        will build a figure of fixed width and height.
        For more in formation on available properties, see the ipywidgets
        documentation on
        `widget layout <https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Styling.html#The-layout-attribute>`_.
    :type layout: dict, optional

    :returns:
        A :class:`gmaps.Figure` widget.

    :Examples:

    >>> import gmaps
    >>> gmaps.configure(api_key="AI...")
    >>> fig = gmaps.figure()
    >>> locations = [(46.1, 5.2), (46.2, 5.3), (46.3, 5.4)]
    >>> fig.add_layer(gmaps.heatmap_layer(locations))

    You can also explicitly specify the intiial map center and zoom:

    >>> fig = gmaps.figure(center=(46.0, -5.0), zoom_level=8)

    To customise the layout:

    >>> fig = gmaps.figure(layout={{
            'width': '400px',
            'height': '600px',
            'padding': '3px',
            'border': '1px solid black'
    }})

    To have a satellite map:

    >>> fig = gmaps.figure(map_type='HYBRID')

    """  # noqa: E501
    if zoom_level is not None or center is not None:
        if zoom_level is None or center is None:
            raise ValueError(
                "Either both zoom_level and center "
                "should be specified, or neither"
            )
        else:
            initial_viewport = InitialViewport.from_zoom_center(
                    zoom_level, center)
    else:
        initial_viewport = InitialViewport.from_data_bounds()

    # set map to occupy entire space allowed by figure
    _map = Map(
        initial_viewport=initial_viewport,
        layout=widgets.Layout(width='100%', height='100%')
    )

    _toolbar = Toolbar() if display_toolbar else None
    _errors_box = ErrorsBox() if display_errors else None
    fig = Figure(
        _map=_map, _toolbar=_toolbar, _errors_box=_errors_box,
        layout=layout, map_type=map_type, tilt=tilt,
        mouse_handling=mouse_handling)
    return fig
