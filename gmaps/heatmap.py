
from IPython.html import widgets
from IPython.utils.traitlets import List, Unicode, Bool

import ipy23_compat
import gmaps_traitlets

class HeatmapWidget(widgets.DOMWidget):
    _view_name = Unicode('HeatmapView', sync=True)
    _bounds = List(sync=True) 
    _data = List(sync=True)
    height = gmaps_traitlets.CSSDimension(sync=True)
    width = gmaps_traitlets.CSSDimension(sync=True)
    max_intensity = ipy23_compat.FloatOrNone(sync=True)
    point_radius = ipy23_compat.FloatOrNone(sync=True)
    _is_weighted = Bool(sync=True)

    def __init__(self, data, height, width, max_intensity, point_radius):
        self._check_data_weighted(data)
        if self._is_weighted:
            self._check_weights_positive(data)
        self._data = data
        self.height = height
        self.width = width
        if max_intensity is not None:
            self.max_intensity = float(max_intensity)
        if point_radius is not None:
            self.point_radius = float(point_radius)
        self._bounds = self._calc_bounds()
        super(widgets.DOMWidget, self).__init__()

    def _check_data_weighted(self, data):
        unique_lengths = set(map(len, data))
        if len(unique_lengths) != 1:
            raise ValueError("Each item in 'data' list must be the same length, either 2 or 3.")
        length = unique_lengths.pop()
        if length == 2:
            self._is_weighted = False
        elif length == 3:
            self._is_weighted = True
        else:
            raise ValueError("Items in 'data' list must be of length 2 "
                    "(for [ latitude, longitude ]) or 3 (for [ latitude, longitude, weight ])")

    def _check_weights_positive(self, data):
        for (latitude, longitude, weight) in data:
            if weight <= 0.0:
                raise ValueError("Google Maps only support positive weights.")

    def _calc_bounds(self):
        min_latitude = min(data[0] for data in self._data)
        min_longitude = min(data[1] for data in self._data)
        max_latitude = max(data[0] for data in self._data)
        max_longitude = max(data[1] for data in self._data)
        return [ (min_latitude, min_longitude), (max_latitude, max_longitude) ]


def heatmap(data, height="400px", width="700px", max_intensity=None, point_radius=None):
    """
    Draw a heatmap of a list of map coordinates.

    Renders a list 'data' of either:
        * pairs of floats denoting (latitude, longitude),
        * triples of floats denoting (latitude, longitude, weight)
    as a heatmap, where the heat denotes point density.

    Arguments
    ---------
    data: list (or Numpy Array) of pairs or triples of floats.
        This is a list of coordinate, possibly associated with a weight. 
        Each element in the list should be a pair 
        (either a list or a tuple) of floats, or a triple
        of floats. The first float should indicate the 
        coordinate's longitude and the second should indicate the 
        coordinate's latitude. If a third float is provided,
        it is interpreted as a weight for that data point.
        Google maps only accepts positive weights.

    Optional arguments
    ------------------
    height: int or string
        Set the height of the map. This can be either an int,
        in which case it is interpreted as a number of pixels, 
        or a string with units like "400px" or "20em".
    width: int or string
        Set the width of the map. This can be either an int,
        in which case it is interpreted as a number of pixels, 
        or a string with units like "400px" or "20em".
    max_intensity: float or None, >= 1.
        Set the maximum intensity of the color gradient. This might
        be useful if the data is highly concentrated in a particular
        area: the heatmap gets very hot in that area and hides the
        detail in the rest of the map. It is also useful if the 
        initial map viewport is very zoomed out. This should, typically,
        be a number between 1 and ~20. By default, the 
        intensity is not capped.
    point_radius: float or None, >= 1.
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

    Or, for a weighted heatmap,
    >>> data = [ [ 37.782551,-122.445368, 2.0 ],
    ...          [ 37.782745,-122.444586, 5.2 ],
    ...          [ 37.782842,-122.443858, 0.2 ] ]
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
