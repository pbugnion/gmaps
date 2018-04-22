
import ipywidgets as widgets

from traitlets import (
    Unicode, List, Enum, Instance, HasTraits,
    Bool, default, observe, Float
)

from . import geotraitlets
from .maps import GMapsWidgetMixin
from .marker import MarkerOptions
from ._docutils import doc_subst


ALLOWED_DRAWING_MODES = {
    'DISABLED', 'MARKER', 'LINE', 'POLYGON', 'DELETE'
}
DEFAULT_DRAWING_MODE = 'MARKER'

DEFAULT_STROKE_COLOR = '#696969'
DEFAULT_FILL_COLOR = '#696969'


_doc_snippets = {}
_doc_snippets['params'] = """
    :param features:
        List of features to draw on the map. Features must be one of
        :class:`gmaps.Marker`, :class:`gmaps.Line` or :class:`gmaps.Polygon`.
    :type features: list of features, optional

    :param marker_options:
        Options controlling how markers are drawn on the map.
        Either pass in an instance of :class:`gmaps.MarkerOptions`,
        or a dictionary with keys `hover_text`, `display_info_box`,
        `info_box_content`, `label` (or a subset of these). See
        :class:`gmaps.MarkerOptions` for documentation on possible
        values. Note that this only affects the initial options
        of markers added to the map by a user. To customise markers
        added programatically, pass in the options to the
        :class:`gmaps.Marker` constructor.
    :type marker_options:
        :class:`gmaps.MarkerOptions`, `dict` or `None`, optional

    :param line_options:
        Options controlling how new lines are drawn on the map.
        Either pass in an instance of :class:`gmaps.LineOptions`,
        or a dictionary with keys `stroke_weight`, `stroke_color`,
        `stroke_opacity` (or a subset of these). See
        :class:`gmaps.LineOptions` for documentation on possible
        values. Note that this only affects the initial options
        of lines added to the map by a user. To customise lines
        added programatically, pass in the options to the
        :class:`gmaps.Line` constructor.
    :type line_options:
        :class:`gmaps.LineOptions`, `dict` or `None`, optional

    :param polygon_options:
        Options controlling how new polygons are drawn on the map. Either pass
        in an instance of :class:`gmaps.PolygonOptions`, or a dictionary with
        keys `stroke_weight`, `stroke_color`, `stroke_opacity`, `fill_color`,
        `fill_opacity` (or a subset of these). See
        :class:`gmaps.PolygonOptions` for documentation on possible values.
        Note that this only affects the initial options of polygons added to
        the map by a user. To customise polygons added programatically, pass in
        the options to the :class:`gmaps.Polygon` constructor.
    :type polygon_options:
        :class:`gmaps.PolygonOptions`, `dict` or `None`, optional
"""

_doc_snippets['examples'] = """
    You can use the drawing layer to add lines, markers and
    polygons to a map:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(features=[
         gmaps.Line((46.23, 5.86), (46.44, 5.24), stroke_weight=3.0),
         gmaps.Marker((46.88, 5.45), label='D'),
         gmaps.Polygon(
             [(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)],
             fill_color='red'
         )
    ])
    >>> fig.add_layer(drawing)
    >>> fig

    You can also use the drawing layer as a way to get user input.
    The user can draw features on the map. You can then get the
    list of features programatically.

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer()
    >>> fig.add_layer(drawing)
    >>> fig
    >>> # Now draw on the map
    >>> drawing.features
    [Marker(location=(46.83, 5.56)),
    Marker(location=(46.46, 5.91)),
    Line(end=(46.32, 5.98), start=(46.42, 5.12))]

    You can bind callbacks that are executed when a new feature is added. For
    instance, you can use `geopy <http://geopy.readthedocs.io/en/latest/>`_ to
    get the address corresponding to markers that you add on the map::

        API_KEY = "Aiz..."

        import gmaps
        import geopy

        gmaps.configure(api_key=API_KEY)
        fig = gmaps.figure()
        drawing = gmaps.drawing_layer()

        geocoder = geopy.geocoders.GoogleV3(api_key=API_KEY)

        def print_address(feature):
            try:
                print(geocoder.reverse(feature.location, exactly_one=True))
            except AttributeError as e:
                # Not a marker
                pass

        drawing.on_new_feature(print_feature)
        fig.add_layer(drawing)
        fig  # display the figure
"""


_doc_snippets['line_options_params'] = """
    :param stroke_color:
        The stroke color of the line. Colors can be specified as a simple
        string, e.g. 'blue', as an RGB tuple, e.g. (100, 0, 0),
        or as an RGBA tuple, e.g. (100, 0, 0, 0.5). Defaults to a grey
        color: (69, 69, 69)
    :type stroke_color: str or tuple, optional

    :param stroke_weight:
        How wide the line is. This is a positive float. Defaults to 2.
    :type stroke_weight: float, optional

    :param stroke_opacity:
        The opacity of the stroke color. The opacity should be a float
        between 0.0 (transparent) and 1.0 (opaque). 0.6 by default.
    :type stroke_opacity: float, optional
"""

_doc_snippets['polygon_options_params'] = """
    {line_options_params}

    :param fill_color:
        The internal color of the polygon. Colors can be specified as a simple
        string, e.g. 'blue', as an RGB tuple, e.g. (100, 0, 0),
        or as an RGBA tuple, e.g. (100, 0, 0, 0.5). Defaults to a grey
        color: (69, 69, 69)
    :type fill_color: str or tuple, optional

    :param fill_opacity:
        The opacity of the fill color. The opacity should be a float
        between 0.0 (transparent) and 1.0 (opaque). 0.2 by default.
    :type fill_opacity: float, optional
""".format(line_options_params=_doc_snippets['line_options_params'].strip())


class DrawingControls(GMapsWidgetMixin, widgets.DOMWidget):
    """
    Widget for the toolbar snippet representing the drawing controls

    :param show_controls:
        Whether the drawing controls should be shown. Defaults to True.
    :type show_controls: bool, optional
    """
    _model_name = Unicode('DrawingControlsModel').tag(sync=True)
    _view_name = Unicode('DrawingControlsView').tag(sync=True)
    show_controls = Bool(default_value=True, allow_none=False).tag(
        sync=True)


@doc_subst(_doc_snippets)
class LineOptions(HasTraits):
    """
    Style options for a line

    Pass an instance of this class to :func:`gmaps.drawing_layer` to
    control the style of new user-drawn lines on the map.

    :Examples:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(
            marker_options=gmaps.MarkerOptions(hover_text='some text'),
            line_options=gmaps.LineOptions(stroke_color='red')
        )
    >>> fig.add_layer(drawing)
    >>> fig # display the figure

    {line_options_params}
    """
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=False, default_value=DEFAULT_STROKE_COLOR
    ).tag(sync=True)
    stroke_weight = Float(
        min=0.0, allow_none=False, default_value=2.0
    ).tag(sync=True)
    stroke_opacity = geotraitlets.Opacity(
        allow_none=False, default_value=0.6).tag(sync=True)

    def to_line(self, start, end):
        new_line = Line(
            start=start,
            end=end,
            stroke_color=self.stroke_color,
            stroke_weight=self.stroke_weight,
            stroke_opacity=self.stroke_opacity
        )
        return new_line


@doc_subst(_doc_snippets)
class Line(GMapsWidgetMixin, widgets.Widget):
    """
    Widget representing a single line on a map

    Add this line to a map via the :func:`gmaps.drawing_layer` function, or by
    passing it directly to the ``.features`` array of an existing instance of
    :class:`gmaps.Drawing`.

    :Examples:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(features=[
         gmaps.Line((46.44, 5.24), (46.23, 5.86), stroke_color='green'),
         gmaps.Line((48.44, 1.32), (47.13, 3.91), stroke_weight=5.0)
    ])
    >>> fig.add_layer(drawing)

    You can also add a line to an existing :class:`gmaps.Drawing`
    instance:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer()
    >>> fig.add_layer(drawing)
    >>> fig # display the figure

    You can now add lines directly on the map:

    >>> drawing.features = [
         gmaps.Line((46.44, 5.24), (46.23, 5.86), stroke_color='green'),
         gmaps.Line((48.44, 1.32), (47.13, 3.91), stroke_weight=5.0)
    ]

    :param start:
        (latitude, longitude) pair denoting the start of the line. Latitudes
        are expressed as a float between -90 (corresponding to 90 degrees
        south) and +90 (corresponding to 90 degrees north). Longitudes are
        expressed as a float between -180 (corresponding to 180 degrees west)
        and +180 (corresponding to 180 degrees east).
    :type start: tuple of floats

    :param end:
        (latitude, longitude) pair denoting the end of the line. Latitudes
        are expressed as a float between -90 (corresponding to 90 degrees
        south) and +90 (corresponding to 90 degrees north). Longitudes are
        expressed as a float between -180 (corresponding to 180 degrees west)
        and +180 (corresponding to 180 degrees east).
    :type start: tuple of floats

    {line_options_params}
    """
    _view_name = Unicode('LineView').tag(sync=True)
    _model_name = Unicode('LineModel').tag(sync=True)
    start = geotraitlets.Point().tag(sync=True)
    end = geotraitlets.Point().tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=False, default_value=DEFAULT_STROKE_COLOR
    ).tag(sync=True)
    stroke_weight = Float(
        min=0.0, allow_none=False, default_value=2.0
    ).tag(sync=True)
    stroke_opacity = geotraitlets.Opacity(
        allow_none=False, default_value=0.6).tag(sync=True)

    def __init__(
            self, start, end,
            stroke_color=DEFAULT_STROKE_COLOR,
            stroke_weight=2.0,
            stroke_opacity=0.6
    ):
        kwargs = dict(
            start=start,
            end=end,
            stroke_color=stroke_color,
            stroke_weight=stroke_weight,
            stroke_opacity=stroke_opacity
        )
        super(Line, self).__init__(**kwargs)


@doc_subst(_doc_snippets)
class PolygonOptions(HasTraits):
    """
    Style options for a polygon.

    Pass an instance of this class to :func:`gmaps.drawing_layer` to
    control the style of new user-drawn polygons on the map.

    :Examples:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(
            polygon_options=gmaps.PolygonOptions(
                stroke_color='red', fill_color=(255, 0, 132))
        )
    >>> fig.add_layer(drawing)
    >>> fig # display the figure

    {polygon_options_params}
    """
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=False, default_value=DEFAULT_STROKE_COLOR
    ).tag(sync=True)
    stroke_weight = Float(
        min=0.0, allow_none=False, default_value=2.0
    ).tag(sync=True)
    stroke_opacity = geotraitlets.Opacity(
        allow_none=False, default_value=0.6).tag(sync=True)
    fill_color = geotraitlets.ColorAlpha(
        allow_none=False, default_value=DEFAULT_FILL_COLOR
    ).tag(sync=True)
    fill_opacity = geotraitlets.Opacity(
        allow_none=False, default_value=0.2).tag(sync=True)

    def to_polygon(self, path):
        new_polygon = Polygon(
            path=path,
            stroke_color=self.stroke_color,
            stroke_weight=self.stroke_weight,
            stroke_opacity=self.stroke_opacity,
            fill_color=self.fill_color,
            fill_opacity=self.fill_opacity
        )
        return new_polygon


@doc_subst(_doc_snippets)
class Polygon(GMapsWidgetMixin, widgets.Widget):
    """
    Widget representing a closed polygon on a map

    Add this polygon to a map via the :func:`gmaps.drawing_layer`
    function, or by passing it directly to the ``.features`` array
    of an existing instance of :class:`gmaps.Drawing`.

    :Examples:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(features=[
         gmaps.Polygon(
            [(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)],
            stroke_color='red', fill_color=(255, 0, 132)
        )
    ])
    >>> fig.add_layer(drawing)

    You can also add a polygon to an existing :class:`gmaps.Drawing`
    instance:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer()
    >>> fig.add_layer(drawing)
    >>> fig # display the figure

    You can now add polygons directly on the map:

    >>> drawing.features = [
         gmaps.Polygon(
             [(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)]
             stroke_color='red', fill_color=(255, 0, 132)
         )
    ]

    :param path:
        List of (latitude, longitude) pairs denoting each point on the polygon.
        Latitudes are expressed as a float between -90 (corresponding to 90
        degrees south) and +90 (corresponding to 90 degrees north). Longitudes
        are expressed as a float between -180 (corresponding to 180 degrees
        west) and +180 (corresponding to 180 degrees east).
    :type path: list of tuples of floats

    {polygon_options_params}
    """
    _view_name = Unicode('PolygonView').tag(sync=True)
    _model_name = Unicode('PolygonModel').tag(sync=True)
    path = List(geotraitlets.Point(), minlen=3).tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha(
        allow_none=False, default_value=DEFAULT_STROKE_COLOR
    ).tag(sync=True)
    stroke_weight = Float(
        min=0.0, allow_none=False, default_value=2.0
    ).tag(sync=True)
    stroke_opacity = geotraitlets.Opacity(
        allow_none=False, default_value=0.6).tag(sync=True)
    fill_color = geotraitlets.ColorAlpha(
        allow_none=False, default_value=DEFAULT_FILL_COLOR
    ).tag(sync=True)
    fill_opacity = geotraitlets.Opacity(
        allow_none=False, default_value=0.2).tag(sync=True)

    def __init__(
            self, path,
            stroke_color=DEFAULT_STROKE_COLOR,
            stroke_weight=2.0,
            stroke_opacity=0.6,
            fill_color=DEFAULT_FILL_COLOR,
            fill_opacity=0.2
    ):
        kwargs = dict(
            path=path,
            stroke_color=stroke_color,
            stroke_weight=stroke_weight,
            stroke_opacity=stroke_opacity,
            fill_color=fill_color,
            fill_opacity=fill_opacity
        )
        super(Polygon, self).__init__(**kwargs)


@doc_subst(_doc_snippets)
class Drawing(GMapsWidgetMixin, widgets.Widget):
    """
    Widget for a drawing layer

    Add this to a :class:`gmaps.Map` or :class:`gmaps.Figure` instance to let
    you draw on the map.

    You should not need to instantiate this directly. Instead, use the
    :func:`gmaps.drawing_layer` factory function.

    :Examples:

    {examples}

    {params}

    :param mode:
        Initial drawing mode. One of ``DISABLED``, ``MARKER``, ``LINE``,
        ``POLYGON`` or ``DELETE``. Defaults to ``MARKER`` if
        ``toolbar_controls.show_controls`` is True, otherwise defaults to
        ``DISABLED``.
    :type mode: str, optional

    :param toolbar_controls:
        Widget representing the drawing toolbar.
    :type toolbar_controls: :class:`gmaps.DrawingControls`, optional
    """
    has_bounds = False
    _view_name = Unicode('DrawingLayerView').tag(sync=True)
    _model_name = Unicode('DrawingLayerModel').tag(sync=True)
    features = List().tag(sync=True, **widgets.widget_serialization)
    mode = Enum(ALLOWED_DRAWING_MODES).tag(sync=True)
    marker_options = widgets.trait_types.InstanceDict(
        MarkerOptions, allow_none=False)
    line_options = widgets.trait_types.InstanceDict(
        LineOptions, allow_none=False)
    polygon_options = widgets.trait_types.InstanceDict(
        PolygonOptions, allow_none=False)
    toolbar_controls = Instance(DrawingControls, allow_none=False).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        kwargs['mode'] = self._get_initial_mode(kwargs)
        if kwargs.get('features') is None:
            kwargs['features'] = []
        if kwargs.get('marker_options') is None:
            kwargs['marker_options'] = self._default_marker_options()
        if kwargs.get('line_options') is None:
            kwargs['line_options'] = self._default_line_options()
        if kwargs.get('polygon_options') is None:
            kwargs['polygon_options'] = self._default_polygon_options()
        self._new_feature_callbacks = []

        super(Drawing, self).__init__(**kwargs)
        self.on_msg(self._handle_message)

    def on_new_feature(self, callback):
        """
        Register a callback called when new features are added

        :param callback:
            Callable to be called when a new feature is added.
            The callback should take a single argument, the
            feature that has been added. This can be an instance
            of :class:`gmaps.Line`, :class:`gmaps.Marker` or
            :class:`gmaps.Polygon`.
        :type callback: callable
        """
        self._new_feature_callbacks.append(callback)

    def _get_initial_mode(self, constructor_kwargs):
        try:
            mode = constructor_kwargs['mode']
        except KeyError:
            # mode not explicitly specified
            controls_hidden = (
                'toolbar_controls' in constructor_kwargs and
                not constructor_kwargs['toolbar_controls'].show_controls
            )
            if controls_hidden:
                mode = 'DISABLED'
            else:
                mode = DEFAULT_DRAWING_MODE
        return mode

    @default('marker_options')
    def _default_marker_options(self):
        return MarkerOptions()

    @default('line_options')
    def _default_line_options(self):
        return LineOptions()

    @default('polygon_options')
    def _default_polygon_options(self):
        return PolygonOptions()

    @default('toolbar_controls')
    def _default_toolbar_controls(self):
        return DrawingControls()

    @observe('features')
    def _on_new_feature(self, change):
        if self._new_feature_callbacks:
            old_features = set(change['old'])
            new_features = [
                feature for feature in change['new']
                if feature not in old_features
            ]
            for feature in new_features:
                for callback in self._new_feature_callbacks:
                    callback(feature)

    def _delete_feature(self, model_id):
        updated_features = [
            feature for feature in self.features
            if feature.model_id != model_id
        ]
        self.features = updated_features

    def _handle_message(self, _, content, buffers):
        if content.get('event') == 'FEATURE_ADDED':
            payload = content['payload']
            if payload['featureType'] == 'MARKER':
                latitude = payload['latitude']
                longitude = payload['longitude']
                feature = self.marker_options.to_marker(latitude, longitude)
            elif payload['featureType'] == 'LINE':
                start = payload['start']
                end = payload['end']
                feature = self.line_options.to_line(start, end)
            elif payload['featureType'] == 'POLYGON':
                path = payload['path']
                feature = self.polygon_options.to_polygon(path)
            self.features = self.features + [feature]
        elif content.get('event') == 'MODE_CHANGED':
            payload = content['payload']
            mode = payload['mode']
            self.mode = mode
        elif content.get('event') == 'FEATURE_DELETED':
            payload = content['payload']
            model_id = payload['modelId']
            self._delete_feature(model_id)


@doc_subst(_doc_snippets)
def drawing_layer(
        features=None, mode=DEFAULT_DRAWING_MODE,
        show_controls=True, marker_options=None, line_options=None,
        polygon_options=None):
    """
    Create an interactive drawing layer

    Adding a drawing layer to a map allows adding custom shapes,
    both programatically and interactively (by drawing on the map).

    :Examples:

    {examples}

    {params}

    :param mode:
        Initial drawing mode. One of ``DISABLED``, ``MARKER``, ``LINE``,
        ``POLYGON`` or ``DELETE``. Defaults to ``MARKER`` if ``show_controls``
        is True, otherwise defaults to ``DISABLED``.
    :type mode: str, optional

    :param show_controls:
        Whether to show the drawing controls in the map toolbar.
        Defaults to True.
    :type show_controls: bool, optional

    :returns:
        A :class:`gmaps.Drawing` widget.
    """
    controls = DrawingControls(show_controls=show_controls)
    kwargs = {
        'features': features,
        'mode': mode,
        'toolbar_controls': controls,
        'marker_options': marker_options,
        'line_options': line_options,
        'polygon_options': polygon_options
    }
    return Drawing(**kwargs)
