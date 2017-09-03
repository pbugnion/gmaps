
import ipywidgets as widgets

from traitlets import Bool, Unicode, CUnicode, List, Enum, observe, validate

from . import geotraitlets
from .locations import locations_to_list
from .maps import GMapsWidgetMixin


ALLOWED_TRAVEL_MODES = {'BICYCLING', 'DRIVING', 'TRANSIT', 'WALKING'}
DEFAULT_TRAVEL_MODE = 'DRIVING'


class DirectionsServiceException(RuntimeError):
    pass


class Directions(GMapsWidgetMixin, widgets.Widget):
    """
    Directions layer.

    Add this to a :class:`gmaps.Figure` instance to draw directions.

    Use the :func:`gmaps.directions_layer` factory function to
    instantiate this class, rather than the constructor.

    :Examples:

    >>> fig = gmaps.figure()
    >>> start = (46.2, 6.1)
    >>> end = (47.4, 8.5)
    >>> waypoints = [(52.37403, 4.88969)]
    >>> directions_layer = gmaps.directions_layer(start, end, waypoints)
    >>> fig.add_layer(directions_layer)

    There is a limitation in the number of waypoints allowed by Google
    (currently 23). If it
    fails to return directions, a ``DirectionsServiceException`` is raised.

    >>> directions_layer = gmaps.Directions(data=data*10)
    Traceback (most recent call last):
        ...
    DirectionsServiceException: No directions returned: MAX WAYPOINTS EXCEEDED

    :param data: List of (latitude, longitude) pairs denoting a single
        point. The first pair denotes the starting point and the last pair
        denote the end of the route.
        Latitudes are expressed as a float between -90
        (corresponding to 90 degrees south) and +90 (corresponding to
        90 degrees north). Longitudes are expressed as a float
        between -180 (corresponding to 180 degrees west) and 180
        (corresponding to 180 degrees east).
    :type data: list of tuples of length >= 2

    :param travel_mode:
        Choose the mode of transport. One of ``'BICYCLING'``, ``'DRIVING'``,
        ``'WALKING'`` or ``'TRANSIT'``. A travel mode of ``'TRANSIT'``
        indicates public transportation. Defaults to ``'DRIVING'``.
    :type travel_mode: str, optional

    :param avoid_ferries: Avoids ferries where possible.
    :type avoid_ferries: bool, optional

    :param avoid_highways: Avoids highways where possible.
    :type avoid_highways: bool, optional

    :param avoid_tolls: Avoids toll roads where possible.
    :type avoid_tolls: bool, optional

    :param optimize_waypoints: Attempt to re-order the supplied intermediate
        waypoints to minimize overall cost of the route.
    :type optimize_waypoints: bool, optional
    """
    has_bounds = True
    _view_name = Unicode("DirectionsLayerView").tag(sync=True)
    _model_name = Unicode("DirectionsLayerModel").tag(sync=True)

    data = List(minlen=2).tag(sync=True)
    data_bounds = List().tag(sync=True)
    avoid_ferries = Bool(default_value=False).tag(sync=True)
    avoid_highways = Bool(default_value=False).tag(sync=True)
    avoid_tolls = Bool(default_value=False).tag(sync=True)
    optimize_waypoints = Bool(default_value=False).tag(sync=True)
    travel_mode = Enum(
            ALLOWED_TRAVEL_MODES,
            default_value=DEFAULT_TRAVEL_MODE
    ).tag(sync=True)

    layer_status = CUnicode().tag(sync=True)

    @validate("data")
    def _validate_data(self, proposal):
        for point in proposal["value"]:
            if not geotraitlets.is_valid_point(point):
                raise geotraitlets.InvalidPointException(
                    "{} is not a valid latitude, longitude pair".format(point))
        return proposal["value"]

    @observe("data")
    def _calc_bounds(self, change):
        data = change["new"]
        min_latitude = min(row[0] for row in data)
        min_longitude = min(row[1] for row in data)
        max_latitude = max(row[0] for row in data)
        max_longitude = max(row[1] for row in data)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]

    @observe("layer_status")
    def _handle_layer_status(self, change):
        if change["new"] != "OK":
            raise DirectionsServiceException(
                "No directions returned: " + change["new"])


def _directions_options(
        start, end, waypoints, travel_mode,
        avoid_ferries, avoid_highways, avoid_tolls,
        optimize_waypoints):
    start = tuple(start)
    end = tuple(end)
    if waypoints is None:
        data = [start, end]
    else:
        data = [start] + locations_to_list(waypoints) + [end]

    model = {
        "data": data,
        "travel_mode": travel_mode,
        "avoid_ferries": avoid_ferries,
        "avoid_highways": avoid_highways,
        "avoid_tolls": avoid_tolls,
        "optimize_waypoints": optimize_waypoints
    }
    return model


def directions_layer(
        start, end, waypoints=None, avoid_ferries=False,
        travel_mode=DEFAULT_TRAVEL_MODE,
        avoid_highways=False, avoid_tolls=False, optimize_waypoints=False):
    """
    Create a directions layer.

    Add this layer to a :class:`gmaps.Figure` instance to draw
    directions on the map.

    :Examples:

    >>> fig = gmaps.figure()
    >>> start = (46.2, 6.1)
    >>> end = (47.4, 8.5)
    >>> directions = gmaps.directions_layer(start, end)
    >>> fig.add_layer(directions)
    >>> fig

    You can also add waypoints on the route:

    >>> waypoints = [(46.4, 6.9), (46.9, 8.0)]
    >>> directions = gmaps.directions_layer(start, end, waypoints=waypoints)

    You can choose the travel mode:

    >>> directions = gmaps.directions_layer(start, end, travel_mode='WALKING')

    :param start:
        (Latitude, longitude) pair denoting the start of the journey.
    :type start: 2-element tuple

    :param end:
        (Latitude, longitude) pair denoting the end of the journey.
    :type end: 2-element tuple

    :param waypoints:
        Iterable of (latitude, longitude) pair denoting waypoints.
        Google maps imposes a limitation on the total number of waypoints.
        This limit is currently 23. You cannot use waypoints when the
        travel_mode is ``'TRANSIT'``.
    :type waypoints: List of 2-element tuples, optional

    :param travel_mode:
        Choose the mode of transport. One of ``'BICYCLING'``, ``'DRIVING'``,
        ``'WALKING'`` or ``'TRANSIT'``. A travel mode of ``'TRANSIT'``
        indicates public transportation. Defaults to ``'DRIVING'``.
    :type travel_mode: str, optional

    :param avoid_ferries:
        Avoid ferries where possible.
    :type avoid_ferries: bool, optional

    :param avoid_highways:
        Avoid highways where possible.
    :type avoid_highways: bool, optional

    :param avoid_tolls:
        Avoid toll roads where possible.
    :type avoid_tolls: bool, optional

    :param optimize_waypoints:
        If set to true, will attempt to re-order the supplied intermediate
        waypoints to minimize overall cost of the route.
    :type optimize_waypoints: bool, optional
    """
    widget_args = _directions_options(
            start, end, waypoints, travel_mode, avoid_ferries,
            avoid_highways, avoid_tolls, optimize_waypoints)
    return Directions(**widget_args)
