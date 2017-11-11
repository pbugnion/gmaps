
import copy
import collections

import ipywidgets as widgets

from traitlets import (
    Unicode, List, Enum, Instance,
    Bool, default, observe
)

from . import geotraitlets
from .maps import GMapsWidgetMixin
from .marker import MarkerOptions
from ._docutils import doc_subst


ALLOWED_DRAWING_MODES = {
    'DISABLED', 'MARKER', 'LINE', 'POLYGON', 'DELETE'
}
DEFAULT_DRAWING_MODE = 'MARKER'


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
        values.
    :type marker_options:
        :class:`gmaps.MarkerOptions`, `dict` or `None`, optional
"""

_doc_snippets['examples'] = """
    You can use the drawing layer to add lines, markers and
    polygons to a map:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(features=[
         gmaps.Line(end=(46.23, 5.86), start=(46.44, 5.24)),
         gmaps.Marker(location=(46.88, 5.45)),
         gmaps.Polygon([(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)])
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


class Line(GMapsWidgetMixin, widgets.Widget):
    """
    Widget representing a single line on a map

    Add this line to a map via the :func:`gmaps.drawing_layer` function, or by
    passing it directly to the ``.features`` array of an existing instance of
    :class:`gmaps.Drawing`.

    :Examples:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(features=[
         gmaps.Line(start=(46.44, 5.24), end=(46.23, 5.86)),
         gmaps.Line(start=(48.44, 1.32), end=(47.13, 3.91))
    ])
    >>> fig.add_layer(drawing)

    You can also add a line to an existing :class:`gmaps.Drawing`
    instance:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer()
    >>> fig # display the figure

    You can now add lines directly on the map:

    >>> drawing.features = [
         gmaps.Line(start=(46.44, 5.24), end=(46.23, 5.86)),
         gmaps.Line(start=(48.44, 1.32), end=(47.13, 3.91))
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
    """
    _view_name = Unicode('LineView').tag(sync=True)
    _model_name = Unicode('LineModel').tag(sync=True)
    start = geotraitlets.Point().tag(sync=True)
    end = geotraitlets.Point().tag(sync=True)

    def __init__(self, start, end):
        kwargs = dict(
            start=start,
            end=end
        )
        super(Line, self).__init__(**kwargs)


class Polygon(GMapsWidgetMixin, widgets.Widget):
    """
    Widget representing a closed polygon on a map

    Add this polygon to a map via the :func:`gmaps.drawing_layer`
    function, or by passing it directly to the ``.features`` array
    of an existing instance of :class:`gmaps.Drawing`.

    :Examples:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer(features=[
         gmaps.Polygon([(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)])
    ])
    >>> fig.add_layer(drawing)

    You can also add a polygon to an existing :class:`gmaps.Drawing`
    instance:

    >>> fig = gmaps.figure()
    >>> drawing = gmaps.drawing_layer()
    >>> fig # display the figure

    You can now add polygons directly on the map:

    >>> drawing.features = [
         gmaps.Polygon([(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)])
    ]

    :param path:
        List of (latitude, longitude) pairs denoting each point on the polygon.
        Latitudes are expressed as a float between -90 (corresponding to 90
        degrees south) and +90 (corresponding to 90 degrees north). Longitudes
        are expressed as a float between -180 (corresponding to 180 degrees
        west) and +180 (corresponding to 180 degrees east).
    :type path: list of tuples of floats
    """
    _view_name = Unicode('PolygonView').tag(sync=True)
    _model_name = Unicode('PolygonModel').tag(sync=True)
    path = List(geotraitlets.Point(), minlen=3).tag(sync=True)

    def __init__(self, path):
        kwargs = dict(path=path)
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
    marker_options = Instance(MarkerOptions, allow_none=False)
    toolbar_controls = Instance(DrawingControls, allow_none=False).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        kwargs['mode'] = self._get_initial_mode(kwargs)
        self._new_feature_callbacks = []

        super(Drawing, self).__init__(**kwargs)
        self.on_msg(self._handle_message)

        # Observe all changes to the marker_options
        # to let users change these directly
        # and still trigger appropriate changes
        self.marker_options.observe(self._on_marker_options_change)

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

    def _on_marker_options_change(self, change):
        self.marker_options = copy.deepcopy(self.marker_options)

    @default('marker_options')
    def _default_marker_options(self):
        return MarkerOptions()

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
                feature = Line(start=start, end=end)
            elif payload['featureType'] == 'POLYGON':
                path = payload['path']
                feature = Polygon(path)
            self.features = self.features + [feature]
        elif content.get('event') == 'MODE_CHANGED':
            payload = content['payload']
            mode = payload['mode']
            self.mode = mode
        elif content.get('event') == 'FEATURE_DELETED':
            payload = content['payload']
            model_id = payload['modelId']
            self._delete_feature(model_id)


def _marker_options_from_dict(options_dict):
    return MarkerOptions(**options_dict)


@doc_subst(_doc_snippets)
def drawing_layer(
        features=None, mode=DEFAULT_DRAWING_MODE,
        show_controls=True, marker_options=None):
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
    if features is None:
        features = []
    controls = DrawingControls(show_controls=show_controls)
    if marker_options is None:
        marker_options = MarkerOptions()
    elif isinstance(marker_options, collections.Mapping):
        marker_options = _marker_options_from_dict(marker_options)
    kwargs = {
        'features': features,
        'mode': mode,
        'toolbar_controls': controls,
        'marker_options': marker_options
    }
    return Drawing(**kwargs)
