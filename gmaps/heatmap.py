
from IPython.html import widgets
from IPython.utils.traitlets import List, Unicode, CFloat

import gmaps_traitlets

class HeatmapWidget(widgets.DOMWidget):
    _view_name = Unicode('HeatmapView', sync=True)
    _bounds = List(sync=True) 
    _data = List(sync=True)
    height = gmaps_traitlets.CSSDimension(sync=True)
    width = gmaps_traitlets.CSSDimension(sync=True)
    max_intensity = CFloat(sync=True, allow_none=True)
    point_radius = CFloat(sync=True, allow_none=True)

    def __init__(self, data, height, width, max_intensity, point_radius):
        self._data = data
        self.height = height
        self.width = width
        self.max_intensity = max_intensity
        self.point_radius = point_radius
        self._bounds = self._calc_bounds()
        super(widgets.DOMWidget, self).__init__()

    def _calc_bounds(self):
        min_latitude = min(data[0] for data in self._data)
        min_longitude = min(data[1] for data in self._data)
        max_latitude = max(data[0] for data in self._data)
        max_longitude = max(data[1] for data in self._data)
        return [ (min_latitude, min_longitude), (max_latitude, max_longitude) ]


def heatmap(data, height="400px", width="700px", max_intensity=None, point_radius=None):
    """
    Draw a heatmap of a list of map coordinates.

    Renders a list 'data' of pairs of floats denoting latitude
    and longitude as a heatmap denoting point density on top of 
    a Google map.

    Arguments
    ---------
    data: list (or Numpy Array) of pairs of floats.
        list of coordinate. Each element in the list should be 
        a pair (either a list or a tuple) of floats. The first 
        float should indicate the coordinate's longitude and
        the second should indicate the coordinate's latitude.

    Optional arguments
    ------------------
    height: int or string
        Set the height of the map. This can be either an int,
        in which case it is interpreted as a number of pixels, 
        or a string with units like "400px" or "20em".
    width: int or string
        Set the height of the map. This can be either an int,
        in which case it is interpreted as a number of pixels, 
        or a string with units like "400px" or "20em".
    max_intensity: Int or None, >= 1.
        Set the maximum intensity of the color gradient. This might
        be useful if the data is highly concentrated in a particular
        area: the heatmap gets very hot in that area and hides the
        detail in the rest of the map. It is also useful if the 
        initial map viewport is very zoomed out. This should, typically,
        be a number between 1 and ~20. By default, the 
        intensity is not capped.
    point_radius: Int or None, >= 1.
        The radius of influence of each data point, in pixels.

    Returns
    -------
    HeatmapWidget
        IPython notebook widget containing the map. Display it
        with a call to 'display'.
    
    Examples
    --------
    >>> data = [ [ 37.782551,-122.445368 ],
    ...          [ 37.782745,-122.444586 ],
    ...          [ 37.782842,-122.443858 ] ]
    >>> w = heatmap(data)
    >>> display(w)
    """
    try:
        data = data.tolist()
    except AttributeError:
        # Not a Numpy Array.
        pass
    w = HeatmapWidget(data, height, width, max_intensity, point_radius)
    return w
