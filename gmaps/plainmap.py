
import ipywidgets as widgets
from traitlets import Unicode, CUnicode, default, Int, List, Tuple, Float

DEFAULT_CENTER = (46.2, 6.1)

class Plainmap(widgets.DOMWidget):
    _view_name = Unicode("PlainmapView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    zoom = Int(8).tag(sync=True)
    center = Tuple(Float(), Float(), default_value=DEFAULT_CENTER).tag(sync=True)

    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')


def plainmap():
    return Plainmap()
