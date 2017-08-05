import ipywidgets as widgets
from traitlets import Unicode

from .maps import GMapsWidgetMixin


class Transit(GMapsWidgetMixin, widgets.Widget):
    """
    Transit layer.

    Add this to a :class:`gmaps.Map` or a :class:`gmaps.Figure`
    instance to add transit (public transport) information.
    This only affects regions for which Google has
    `transit information
    <https://www.google.com/landing/transit/cities/index.html>`_.

    You should not instantiate this directly. Instead,
    use the :func:`gmaps.transit_layer` factory function.

    :Examples:

    ::

        # map centered on London
        >>> fig = gmaps.figure(center=(51.5, -0.2), zoom_level=11)
        >>> fig.add_layer(gmaps.transit_layer())
        >>> fig
    """
    _view_name = Unicode('TransitLayerView').tag(sync=True)
    _model_name = Unicode('TransitLayerModel').tag(sync=True)
    has_bounds = False


def transit_layer():
    """
    Transit layer.

    Adds information about public transport lines to the
    map. This only affects region for which Google has
    `public transport information
    <https://www.google.com/landing/transit/cities/index.html>`_.

    :returns:
        A :class:`gmaps.Transit` widget.

    :Examples:

    ::

        # map centered on London
        >>> fig = gmaps.figure(center=(51.5, -0.2), zoom_level=11)
        >>> fig.add_layer(gmaps.transit_layer())
        >>> fig
    """
    return Transit()
