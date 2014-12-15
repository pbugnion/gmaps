
from IPython.html import widgets
from IPython.utils.traitlets import List, Unicode

import gmaps_traitlets

class PlainmapWidget(widgets.DOMWidget):
	_view_name = Unicode("PlainmapView", sync=True)
	_bounds = List(sync=True)
	height = gmaps_traitlets.CSSDimension(sync=True)
	width = gmaps_traitlets.CSSDimension(sync=True)

	def __init__(self, height, width):
		self.height = height
		self.width = width
		self._bounds = [ [ 10., 10. ], [20., 20.] ]
		super(widgets.DOMWidget, self).__init__()


def plainmap(height="400px", width="700px"):
	w = PlainmapWidget(height, width)
	return w