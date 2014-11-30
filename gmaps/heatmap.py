
from IPython.html import widgets # Widget definitions
from IPython.utils.traitlets import List, Unicode # Used to declare attributes of our widget

class HeatmapWidget(widgets.DOMWidget):
    _view_name = Unicode('HeatmapView', sync=True)
    _bounds = List(sync=True) 
    _data = List(sync=True)

    def __init__(self, data):
        self._data = data
        self._bounds = self._calc_bounds()
        self.width = "800px"
        self.height = "400px"
        super(widgets.DOMWidget, self).__init__()

    def _calc_bounds(self):
        min_latitude = min(data[0] for data in self._data)
        min_longitude = min(data[1] for data in self._data)
        max_latitude = max(data[0] for data in self._data)
        max_longitude = max(data[1] for data in self._data)
        return [ (min_latitude, min_longitude), (max_latitude, max_longitude) ]


