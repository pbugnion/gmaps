import math


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
    lower_bound = max(mean - 2.0*standard_deviation, -89.9)
    upper_bound = min(mean + 2.0*standard_deviation, 89.9)
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
    mean = sum(longitudes) / N
    radians = [math.radians(longitude) for longitude in longitudes]
    sum_cos = sum(math.cos(r) for r in radians)**2
    sum_sin = sum(math.sin(r) for r in radians)**2
    Rsq = (1/N**2) * (sum_cos+sum_sin)
    standard_deviation = math.sqrt(-math.log(Rsq))
    extent = 2.0*math.degrees(standard_deviation)
    extent = min(extent, 180)

    # centre the bound within [-180, 180]
    lower_bound = ((mean - extent + 180.0) % 360.0) - 180.0
    upper_bound = ((mean + extent + 180.0) % 360.0) - 180.0
    return lower_bound, upper_bound
