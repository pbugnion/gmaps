
def locations_to_list(locations):
    """
    Convert from a generic iterable of locations to a list of tuples

    Layer widgets only accepts lists of tuples, but we want the user
    to be able to pass in any reasonable iterable. We therefore
    need to convert the iterable passed in.
    """
    try:
        location_tuples = locations.itertuples()  # locations is a dataframe
        locations_as_list = [
            (latitude, longitude) for (idx, latitude, longitude)
            in location_tuples
        ]
    except AttributeError:
        locations_as_list = [
            (latitude, longitude) for (latitude, longitude)
            in locations
        ]
    return locations_as_list


locations_docstring = """
    :param locations:
        Iterable of (latitude, longitude) pairs denoting a single point.
        Latitudes are expressed as a float between -90 (corresponding to 90
        degrees south) and +90 (corresponding to 90 degrees north). Longitudes
        are expressed as a float between -180 (corresponding to 180 degrees
        west) and +180 (corresponding to 180 degrees east). This can be passed
        in as either a list of tuples, a two-dimensional numpy array or a
        pandas dataframe with two columns, in which case the first one is taken
        to be the latitude and the second one is taken to be the longitude.
    :type locations: iterable of latitude, longitude pairs
"""
