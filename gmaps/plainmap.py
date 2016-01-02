
from ._ipywidgets import widgets
from ._traitlets import List, Unicode

import gmaps.gmaps_traitlets as gmaps_traitlets

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
	"""
	Draw a simple map.

	This is currently experimental and should be used with
	caution.
	"""
	w = PlainmapWidget(height, width)
	return w
