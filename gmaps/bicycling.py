import ipywidgets as widgets
from traitlets import Unicode

from .maps import GMapsWidgetMixin


class Bicycling(GMapsWidgetMixin, widgets.Widget):
    """
    Bicycling layer.

    Add this to a :class:`gmaps.Map` or :class:`gmaps.Figure`
    instance to add cycling routes.

    You should not instantiate this directly. Instead,
    use the :func:`gmaps.bicycling_layer` factory function.

    :Examples:

    >>> fig = gmaps.figure()
    >>> fig.add_layer(gmaps.bicycling_layer())
    """
    _view_name = Unicode('BicyclingLayerView').tag(sync=True)
    _model_name = Unicode('BicyclingLayerModel').tag(sync=True)
    has_bounds = False


def bicycling_layer():
    """
    Bicycling layer.

    Adds cycle routes and decreases the weight of main routes
    on the map.

    :returns:
        A :class:`gmaps.Bicycling` widget.

    :Examples:

    >>> fig = gmaps.figure()
    >>> fig.add_layer(gmaps.bicycling_layer())
    """
    return Bicycling()
