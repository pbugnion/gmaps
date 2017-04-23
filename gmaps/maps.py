
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
# For example: (170,-170) means we cover 20 degrees of
# latitude starting at 170 (through 180)
# Whereas (-170,170) means we start where the previous
# interval ended (at 170), go through lng 0, and eventually
# to 170 (340 degrees).
#
# As a side note, this definition means that (lng1,lng0) is
# the complement of (lng0,lng1) on this notation.
# It is important we have this direction information somehow,
# because otherwise the bounds are underspecified.
#
# As another side note, the meaning of (15, 30) in this notation
# is the same as that of (15+/-360, 30) and that of (15, 30 +/- 360),
# because we stop as soon as we hit the coordinate the first
# time.
#
# Note: the google api for setting map bounds seems to follow this
# convention as well, but I'm not sure gmaps overall does.
# (At least, I couldn't verify)
#
#-180                                            180 = -180
# |     >--------------->                        |
# |         >------->                            |
# |            >------------->                   |
# |->    >------->                         >-----|
# 11000012223334433322221111100000000000000111111|
#                            ^ biggest empty range
# the bounds are then
#  First we find which longitude ranges are feasible
#  to cut (they have no range overlaps) by counting number of
#  intervals that overlap and finding 0s.
#  The initial condition (at -180)
#  we find from counting how many intervals have west > east.
#  then we go through our list.
#  Of all the segments with a 0 count, the longest one
#  is the one we should use to cut the map (here we
#  have two choices)

#
def normalize_lng(lng):
    """ returns an equivalent longitude in the [-180,180) range """
    lng = lng % 360
    if lng >= 180:
        lng = lng - 360

    assert(lng >= -180)
    assert(lng < 180)
    return lng


# Then we can search for the best gap, including ones that wrap around
# we achieve this by sorting and counting covering intervals
# 0 means no bounds overalp with that segment
def get_lng_bound(bounds_list):

    # extract and normalize lngs from bounds (if they arent normalized)
    directed_intervals = [(normalize_lng(b[0][1]),
                           normalize_lng(b[1][1]))
                          for b in bounds_list]

    # coverage is initially the number of wrap-around intervals. it can be 0.
    coverage = sum([1 for (lng0, lng1)
                    in directed_intervals if lng0 > lng1])
    
    starts = [(lng_start, 1)
              for (lng_start, _) in directed_intervals]

    ends = [(lng_end, -1)
            for (_, lng_end) in directed_intervals]

    endpoints = starts + ends
    endpoints += [(x + 360, i)
                  for (x, i) in endpoints]
    # we repeat the longs shifted by 360 to handle gaps that overlap with 180
    # without special-casing. 
    interleaved = sort(endpoints)

    # The largest clear gap we know of.
    # We start by assuming there isn't one.
    largest_gap = (-180, -180)
    # current segment starts as -180
    seg_start = -180
    for (bnd, delta) in interleaved:
        if coverage == 0 and
        (bnd - seg_start) > (largest_gap[1] - largest_gap[0]):
            largest_gap = (seg_start, bnd)
        seg_start = bnd
        coverage += delta
        assert(coverage >= 0)

    # reversing the lng order in a gap gives us a valid bound
    # the largest gap has the smallest bound
    return (normalize_lng(largest_gap[1]),
            normalize_lng(largest_gap[0]))


class Map(widgets.DOMWidget, ConfigurationMixin):

    """
    Base map class

    Instances of this act as a base map on which you can add
    additional layers.

    :Examples:

    >>> m = gmaps.Map()
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
