
from IPython.display import Javascript, display

__has_initialized__ = False

def init():
    # FIXME
    # Loads the JS extensions. This is still a bit of a 
    # hack: calls to gmaps methods cannot occur in the 
    # same cell as the import statement. 
    #
    # Potential alternatives would be to re-factor the 
    # init statement into a line magic.
    global __has_initialized__
    if not __has_initialized__:
        display(Javascript("""
            IPython.load_extensions('gmaps_js/heatmap_view')
            """))
        __has_initialized__ = True

