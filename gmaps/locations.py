
def locations_to_list(locations):
    """
    Convert from a generic iterable of locations to a list of tuples

    The widget only accepts lists of tuples, but we want the user
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
