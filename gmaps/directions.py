
import ipywidgets as widgets

from traitlets import Unicode, CUnicode, List, observe, validate

from . import geotraitlets
from .locations import locations_to_list


class DirectionsServiceException(RuntimeError):
    pass


class Directions(widgets.Widget):
    """
    Directions layer.

    Add this to a ``Map`` instance to draw directions.

    The directions are requested with the ``DRIVING`` option.

    Data is a list of latitude, longitude tuples. The first point of the list
    is passed as the origin of the itinerary and the last point is passed as
    the destination of the itinerary. Other points are passed in order as a
    list of waypoints.

    :Examples:

    >>> m = gmaps.Map()
    >>> data = [(48.85341, 2.3488), (50.85045, 4.34878), (52.37403, 4.88969)]
    >>> directions_layer = gmaps.Directions(data=data)
    >>> m.add_layer(directions_layer)

    There is a limitation in the number of waypoints allowed by Google
    (currently 23). If it
    fails to return directions, a DirectionsServiceException is raised.

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
    """
    has_bounds = True
    _view_name = Unicode("DirectionsLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("DirectionsLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    data = List(minlen=2).tag(sync=True)
    data_bounds = List().tag(sync=True)

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


def _directions_options(start, end, waypoints):
    start = tuple(start)
    end = tuple(end)
    if waypoints is None:
        data = [start, end]
    else:
        data = [start] + locations_to_list(waypoints) + [end]
    return {"data": data}


def directions_layer(start, end, waypoints=None):
    widget_args = _directions_options(start, end, waypoints)
    return Directions(**widget_args)
