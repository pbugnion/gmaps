import ipywidgets as widgets

from traitlets import Unicode, Bool

from .maps import GMapsWidgetMixin


class Traffic(GMapsWidgetMixin, widgets.Widget):
    """
    Traffic layer

    Add this to a :class:`gmaps.Map` or a :class:`gmaps.Figure`
    instance to add traffic information to the map, where
    supported.

    You should not instantiate this directly. Instead,
    use the :func:`gmaps.traffic_layer` factory function.

    :Examples:

    ::

        # map centered on London
        >>> fig = gmaps.figure(center=(51.5, -0.2), zoom_level=11)
        >>> fig.add_layer(gmaps.traffic_layer())
        >>> fig

    :param auto_refresh:
        Whether the traffic layer refreshes with updated
        information automatically. This is true by default.
    :type auto_refresh: bool, optional
    """
    _view_name = Unicode('TrafficLayerView').tag(sync=True)
    _model_name = Unicode('TrafficLayerModel').tag(sync=True)
    auto_refresh = Bool(True).tag(sync=True)
    has_bounds = False


def traffic_layer(auto_refresh=True):
    """
    Traffic layer.

    Adds information about the current state of traffic
    to the map. This layer only works at sufficiently high
    zoom levels, and for regions for which Google Maps
    has traffic information.

    :param auto_refresh:
        Whether the traffic layer refreshes with updated
        information automatically. This is true by default.
    :type auto_refresh: bool, optional

    :returns:
        A :class:`gmaps.Traffic` widget.

    :Examples:

    ::

        # map centered on London
        >>> fig = gmaps.figure(center=(51.5, -0.2), zoom_level=11)
        >>> fig.add_layer(gmaps.traffic_layer())
        >>> fig
    """
    return Traffic(auto_refresh=auto_refresh)
