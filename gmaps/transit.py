import ipywidgets as widgets
from traitlets import Unicode


class Transit(widgets.Widget):
    _view_name = Unicode('TransitLayerView').tag(sync=True)
    _view_module = Unicode('jupyter-gmaps').tag(sync=True)
    _model_name = Unicode('TransitLayerModel').tag(sync=True)
    _model_module = Unicode('jupyter-gmaps').tag(sync=True)
    has_bounds = False


def transit_layer():
    """
    Transit layer.

    Adds information about public transport lines to the
    map. This only affects region for which Google has
    `public transport information
    <https://www.google.com/landing/transit/cities/index.html>`_.

    :Examples:

    ::

        # map centered on London
        >>> fig = gmaps.figure(center=(51.5, -0.2), zoom_level=11)
        >>> fig.add_layer(gmaps.transit_layer())
        >>> fig
    """
    return Transit()
