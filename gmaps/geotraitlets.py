
import traitlets

class Latitude(traitlets.Float):
    """
    Float representing a latitude

    Latitude values must be between -90 and 90.
    """
    info_text = "a valid latitude (-90 <= latitude <= 90)"
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        if -90.0 <= value <= 90.0:
            return value
        else:
            self.error(obj, value)


class Longitude(traitlets.Float):
    """
    Float representing a longitude

    Longitude values must be between -180 and 180.
    """
    info_text = "a valid longitude (-180 <= longitude <= 180)"
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        if -180.0 <= value <= 180.0:
            return value
        else:
            self.error(obj, value)


class Point(traitlets.Tuple):
    """
    Tuple representing a (latitude, longitude) pair.
    """
    info_text = "a valid (latitude, longitude) pair"

    def __init__(self, default_value):
        super(Point, self).__init__(
            Latitude(), Longitude(), default_value=default_value)


def is_valid_point(pt):
    latitude, longitude = pt
    return (-90.0 <= latitude <= 90.0) and (-180.0 <= longitude <= 180.0)
