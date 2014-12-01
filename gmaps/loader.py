
from IPython.display import Javascript, display
import os
import sys

__has_initialized__ = False

js_libnames = ["heatmap_view.js"]

def init():
    global __has_initialized__
    if not __has_initialized__:
        js = """
        window.gmap_initialize = function() {};
        $.getScript('https://maps.googleapis.com/maps/api/js?v=3&sensor=false&libraries=visualization&callback=gmap_initialize');
        """
        __has_initialized__ = True
        #display(Javascript(data=js))
        #_load_jslibs()

def _load_jslibs():
    # Maybe this should be refactored to use nbextensions?
    self_module = sys.modules[__name__]
    self_path = os.path.dirname(self_module.__file__)
    path_to_libs = os.path.join(self_path, "js")
    for libname in js_libnames:
        with open(os.path.join(path_to_libs, libname)) as f:
            display(Javascript(f.read()))

