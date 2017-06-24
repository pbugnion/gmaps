import math


EPSILON = 1e-5


def latitude_bounds(latitudes):
    """
    Estimate latitude bound with 2*sample standard deviation
    """
    N = float(len(latitudes))
    mean = sum(latitudes) / N
    sum_squares = sum(
        (latitude-mean)**2 for latitude in latitudes
    )
    standard_deviation = math.sqrt(sum_squares/float(N))
    lower_bound = max(mean - 2.0*standard_deviation, -(90.0 - EPSILON))
    upper_bound = min(mean + 2.0*standard_deviation, (90.0 - EPSILON))
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
    N = float(len(longitudes))
    radians = [math.radians(longitude) for longitude in longitudes]
    sum_cos = sum(math.cos(r) for r in radians)
    sum_cos_sq = sum_cos**2
    sum_sin = sum(math.sin(r) for r in radians)
    sum_sin_sq = sum_sin**2
    mean_radians = math.atan2(sum_sin, sum_cos)
    mean_degrees = math.degrees(mean_radians)
    Rsq = (1/N**2) * (sum_cos_sq + sum_sin_sq)
    standard_deviation = math.sqrt(-math.log(Rsq))
    extent = 2.0*math.degrees(standard_deviation)
    extent = min(extent, 180.0 - EPSILON)

    # centre the bound within [-180, 180]
    lower_bound = ((mean_degrees - extent + 180.0) % 360.0) - 180.0
    upper_bound = ((mean_degrees + extent + 180.0) % 360.0) - 180.0
    return lower_bound, upper_bound
