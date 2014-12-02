
from IPython.html import widgets
from IPython.utils.traitlets import List, Unicode

import gmaps_traitlets

class HeatmapWidget(widgets.DOMWidget):
    _view_name = Unicode('HeatmapView', sync=True)
    _bounds = List(sync=True) 
    _data = List(sync=True)
    height = gmaps_traitlets.CSSDimension(sync=True)
    width = gmaps_traitlets.CSSDimension(sync=True)

    def __init__(self, data, height, width):
        self._data = data
        self.height = height
        self.width = width
        self._bounds = self._calc_bounds()
        super(widgets.DOMWidget, self).__init__()

    def _calc_bounds(self):
        min_latitude = min(data[0] for data in self._data)
        min_longitude = min(data[1] for data in self._data)
        max_latitude = max(data[0] for data in self._data)
        max_longitude = max(data[1] for data in self._data)
        return [ (min_latitude, min_longitude), (max_latitude, max_longitude) ]


def heatmap(data, height="400px", width="700px"):
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
    w = HeatmapWidget(data, height, width)
    return w
