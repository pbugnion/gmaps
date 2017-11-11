import math


EPSILON = 1e-5

# GoogleMaps imposes latitude restrictions
MAX_ALLOWED_LATITUDE = 85.0
MIN_ALLOWED_LATITUDE = -85.0


def latitude_bounds(latitudes):
    """
    Estimate latitude bound with 2*sample standard deviation
    """
    if max(latitudes) - min(latitudes) < 2.0*EPSILON:
        lower_bound = latitudes[0] - EPSILON
        upper_bound = latitudes[0] + EPSILON
    else:
        N = float(len(latitudes))
        mean = sum(latitudes) / N
        sum_squares = sum(
            (latitude-mean)**2 for latitude in latitudes
        )
        standard_deviation = math.sqrt(sum_squares/float(N))
        lower_bound = max(mean - 2.0*standard_deviation, -(90.0 - EPSILON))
        upper_bound = min(mean + 2.0*standard_deviation, (90.0 - EPSILON))
    lower_bound, upper_bound = _constrain_latitude_bounds(
        lower_bound, upper_bound)
    return lower_bound, upper_bound


def longitude_bounds(longitudes):
    """
    Estimate longitude bound with 2*sample standard deviation

    Note that longitudes wrap around, so have to use parameter
    estimation for wrapped probability distribution.

    See https://en.wikipedia.org/wiki/Wrapped_normal_distribution
    and https://en.wikipedia.org/wiki/Directional_statistics
    for how to calculate the relevant statistics.
    """
    normalized_longitudes = [
        _normalize_longitude(longitude) for longitude in longitudes
    ]
    if max(normalized_longitudes) - min(normalized_longitudes) < 2.0*EPSILON:
        mean_longitude = 0.5 * (
            max(normalized_longitudes) + min(normalized_longitudes)
        )
        upper_bound = mean_longitude + EPSILON
        lower_bound = mean_longitude - EPSILON
    else:
        N = float(len(longitudes))
        radians = [
            math.radians(longitude) for longitude in normalized_longitudes
        ]
        sum_cos = sum(math.cos(r) for r in radians)
        sum_cos_sq = sum_cos**2
        sum_sin = sum(math.sin(r) for r in radians)
        sum_sin_sq = sum_sin**2
        mean_radians = math.atan2(sum_sin, sum_cos)
        mean_degrees = math.degrees(mean_radians)
        Rsq = (1/N**2) * (sum_cos_sq + sum_sin_sq)
        standard_deviation = math.sqrt(-math.log(Rsq))
        extent = 2.0*math.degrees(standard_deviation)
        if extent > 180.0:
            # longitudes cover entire map
            upper_bound = 180.0 - EPSILON
            lower_bound = -upper_bound
        else:
            lower_bound = _normalize_longitude(mean_degrees - extent)
            upper_bound = _normalize_longitude(mean_degrees + extent)
    return lower_bound, upper_bound


def merge_longitude_bounds(longitude_bounds_list):
    """
    Return a single set of bounds that encompasses a list of bounds
    """

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
    # -180                                            180 = -180
    #   |     >--------------->                        |
    #   |         >------->                            |
    #   |            >------------->                   |
    #   |->    >------->                         >-----|
    #   11000012223334433322221111100000000000000111111|
    #                              ^ biggest empty range
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
    # extract and normalize lngs from bounds (if they arent normalized)
    directed_intervals = [
        (_normalize_longitude(lower), _normalize_longitude(upper))
        for lower, upper in longitude_bounds_list
    ]

    # coverage is initially the number of wrap-around intervals. it can be 0.
    coverage = sum(1 for lower, upper in directed_intervals if lower > upper)

    starts = [(lower, 1) for (lower, _) in directed_intervals]

    ends = [(upper, -1) for (_, upper) in directed_intervals]

    endpoints = starts + ends
    endpoints += [(x + 360, i) for (x, i) in endpoints]

    # we repeat the longs shifted by 360 to handle gaps that overlap with 180
    # without special-casing.
    interleaved = sorted(endpoints)

    # The largest clear gap we know of.
    # We start by assuming there isn't one.
    largest_gap = (-180.0, -180.0)
    # current segment starts as -180
    seg_start = -180.0
    for (bnd, delta) in interleaved:
        if coverage == 0 \
          and (bnd - seg_start) > (largest_gap[1] - largest_gap[0]):
            largest_gap = (seg_start, bnd)
        seg_start = bnd
        coverage += delta
        assert(coverage >= 0)

    # reversing the lng order in a gap gives us a valid bound
    # the largest gap has the smallest bound
    upper, lower = largest_gap
    return _normalize_longitude(lower), _normalize_longitude(upper)


def _normalize_longitude(longitude):
    """ An equivalent longitude in the [-180,180) range """
    longitude = longitude % 360
    if longitude >= 180:
        longitude = longitude - 360

    return longitude


def _constrain_latitude_bounds(lower_bound, upper_bound):
    if lower_bound < MIN_ALLOWED_LATITUDE:
        lower_bound = MIN_ALLOWED_LATITUDE
        if upper_bound < lower_bound + EPSILON:
            upper_bound = lower_bound + EPSILON
    if upper_bound > MAX_ALLOWED_LATITUDE:
        upper_bound = MAX_ALLOWED_LATITUDE
        if lower_bound > upper_bound - EPSILON:
            lower_bound = upper_bound - EPSILON
    return lower_bound, upper_bound
