
import ipywidgets as widgets
from traitlets import (Unicode, default, List, Tuple, Instance,
                       observe, Dict, HasTraits)

DEFAULT_CENTER = (46.2, 6.1)
DEFAULT_BOUNDS = [(46.2, 6.1), (47.2, 7.1)]

_default_configuration = {"api_key": None}


def configure(api_key=None):
    """
    Configure access to the GoogleMaps API.

    :param api_key: String denoting the key to use when accessing Google maps,
        or None to not pass an API key.
    """
    configuration = {"api_key": api_key}
    global _default_configuration
    _default_configuration = configuration


class ConfigurationMixin(HasTraits):
    configuration = Dict(
        traits={"api_key": Unicode(allow_none=True)}).tag(sync=True)

    @default("configuration")
    def _config_default(self):
        return _default_configuration



# I assume (lng0, lng1) in a layer's
# bounds means that the layer wants the map to
# cover all the longitudes that lie
# (going eastwards) from lng0 to lng1.
# For example: (170,-170) means we cover 20 degrees of latitude starting at 170 (through 180)
# Wherease (-170,170) means we start where the previous one ended, go through 0, eventually to 170 (340 degrees)
# This means that (lng1,lng0) is the complement of (lng0,lng1) on this notation.
# It is important we have this sense information somehow, because otherwise the bounds are
# underspecified.
# Note: the google api for setting map bounds seems to follow this convention as well

# then, given a set of bounds we want to satisfy,
# we want to exclude the largest stretch of remaining map possible
# while satisfying all bounds. We can do this by finding the
# largest gap that has no bounds on it.
#
# To do this easily despite the wrap-around, we can normalize
# all our input bounds to make sure that lng_start < lng_end
# for each bound set as follows:
#
# 1) normalize every given bound such that
#    * -180 < lng_start  < 180
#    * long_start < long_end
#    * long_start + 360 > long_end
# We can do this by adding a multiple of 360 to either bound
# Sort all start / ends (labelled as such)
# find places where no interval is covering
# find the largest such place, the bounds are the complement of this interval
# 
#
def normalize_lng_bound(lng_start, lng_end):
    """ returns an equivalent bound with nice properties to work with """
    lng_start = lng_start % 360
    if lng_start >= 180:
        lng_start -= 360

    lng_end = lng_end % 360
    if lng_end >= lng_start + 360:
        lng_end -= 360

    if lng_end < lng_start:
        lng_end += 360

    assert(-180 <= lng_start)
    assert(lng_start < 180)
    assert(lng_end >= lng_start)
    assert(lng_end < 360 + lng_start)

    return (lng_start, lng_end)


# Then we can search for the best gap, including ones that wrap around
# we achieve this by sorting and counting covering intervals
# 0 means no bounds overalp with that segment
def get_lng_bound(bounds_list):
    directed_intervals = [(b[0][1], b[1][1]) for b in bounds_list]
    normalized_lngs = [normalize_lng_bound(lng1,lng2) for (lng1,lng2) in directed_intervals]
    starts = [(lng_start, 1) for (lng_start, _) in normalized_lngs]
    ends = [(lng_end, -1) for (_, lng_end) in normalized_lngs]
    interleaved = sorted(starts + ends)
    (curr_seg_start, coverage) = (-180,0)
    best_gap = (-180,-180)
    for (bnd, delta) in interleaved:
        if coverage == 0 and (bnd - curr_seg_start > best_gap[1] - best_gap[0]):
            best_gap = (curr_seg_start, bnd)

        (curr_seg_start, coverage) = (bnd, coverage + delta)

    # once we found the best gap, the best bounds are the complement
    # we normalize for readability
    best_bounds = normalize_lng_bound(best_gap[1],best_gap[0])
    return best_bounds


class Map(widgets.DOMWidget, ConfigurationMixin):
    """
    Base map class

    Instances of this act as a base map on which you can add
    additional layers.

    You should use the :func:`gmaps.figure` factory method
    to instiate a figure, rather than building this class
    directly.

    :Examples:

    >>> m = gmaps.figure()
    >>> m.add_layer(gmaps.heatmap_layer(locations))
    """
    _view_name = Unicode("PlainmapView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("PlainmapModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)
    layers = Tuple(trait=Instance(widgets.Widget)).tag(
        sync=True, **widgets.widget_serialization)
    data_bounds = List(DEFAULT_BOUNDS).tag(sync=True)

    def add_layer(self, layer):
        self.layers = tuple([l for l in self.layers] + [layer])

    @default("layout")
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    @observe("layers")
    def _calc_bounds(self, change):
        layers = change["new"]
        bounds_list = [
            layer.data_bounds for layer in layers if layer.has_bounds
        ]
        if bounds_list:
            min_latitude = min(bounds[0][0] for bounds in bounds_list)
            max_latitude = max(bounds[1][0] for bounds in bounds_list)

            (min_longitude, max_longitude) = get_lng_bound(bounds_list)

            self.data_bounds = [
                (min_latitude, min_longitude),
                (max_latitude, max_longitude)
            ]
