
import IPython
from IPython.html import widgets
from IPython.utils.traitlets import List, Unicode

class HeatmapWidget(widgets.DOMWidget):
    _view_name = Unicode('HeatmapView', sync=True)
    _bounds = List(sync=True) 
    _data = List(sync=True)
    height = Unicode(sync=True)
    width = Unicode(sync=True)

    def __init__(self, data):
        self._data = data
        self._bounds = self._calc_bounds()
        self.width = "800px"
        self.height = "400px"
        if IPython.version_info[0] == 2:
            self._css = { "height" : self.height, "width" : self.width }
        super(widgets.DOMWidget, self).__init__()

    def _calc_bounds(self):
        min_latitude = min(data[0] for data in self._data)
        min_longitude = min(data[1] for data in self._data)
        max_latitude = max(data[0] for data in self._data)
        max_longitude = max(data[1] for data in self._data)
        return [ (min_latitude, min_longitude), (max_latitude, max_longitude) ]


def heatmap(data):
    """
    Draw a heatmap of a list of map coordinates.

    Renders a list 'data' of pairs of floats denoting latitude
    and longitude as a heatmap denoting point density on top of 
    a Google map.

    Arguments
    ---------
    data: list of pairs of floats.
        list of coordinate. Each element in the list should be 
        a pair (either a list or a tuple) of floats. The first 
        float should indicate the coordinate's longitude and
        the second should indicate the coordinate's latitude.

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
    w = HeatmapWidget(data)
    return w
