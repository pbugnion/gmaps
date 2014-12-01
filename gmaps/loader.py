
from IPython.display import Javascript, display
import os
import sys

__has_initialized__ = False

js_libnames = ["heatmap_view.js"]

def init():
    global __has_initialized__
    if not __has_initialized__:
        display(Javascript("""
            IPython.load_extensions('js/heatmap_view')
            """))
        __has_initialized__ = True

