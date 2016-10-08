
import re

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


_color_names = {
    "black", "silver", "gray", "white", "maroon", "red",
    "purple", "fuschia", "green", "lime", "olive",
    "yellow", "navy", "blue", "teal", "aqua"
}

_color_re = re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$')
_rgb_re = re.compile(r'rgb\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3}\)')
_rgba_re = re.compile(r'rgba\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3},0?\.[0-9]*\)')


class ColorString(traitlets.Unicode):
    """
    A string holding a color recognized by Google Maps.

    Apparently Google Maps accepts 'all CSS3 colors, including
    RGBA, [...] except for extended named colors and HSL(A)
    values'.

    Using `this <https://www.w3.org/TR/css3-color/#html4>` page
    for reference.
    """
    info_text = 'an HTML color recognized by Google maps'
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        try:
            value_as_string = super(ColorString, self).validate(obj, value)
            normalised_string = value_as_string.replace(" ", "").lower()
            if (
                normalised_string.lower() in _color_names or
                _color_re.match(normalised_string) or
                _rgb_re.match(normalised_string) or
                _rgba_re.match(normalised_string)
            ):
                return normalised_string
            else:
                return self.error(obj, value)
        except TypeError:
            return self.error(obj, value)


class RgbTuple(traitlets.Tuple):
    info_text = "a triple of integers between 0 and 255 like (100, 0, 250)"

    def __init__(self, **metadata):
        traits = [
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255)
        ]
        super(RgbTuple, self).__init__(*traits, **metadata)


class RgbaTuple(traitlets.Tuple):
    info_text = "an RGBA tuple like (100, 0, 250, 0.5)"

    def __init__(self, **metadata):
        traits = [
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Float(traitlets.Undefined, min=0.0, max=1.0)
        ]
        super(RgbaTuple, self).__init__(*traits, **metadata)


class ColorAlpha(traitlets.Union):
    """
    Trait representing a color that can be passed to Google maps.

    This is either a string like 'blue' or '#aabbcc' or an RGB
    tuple like (100, 0, 250) or an RGBA tuple like (100, 0, 250, 0.5).
    """
    def __init__(
            self, default_value=traitlets.Undefined,
            allow_none=False, **metadata):
        trait_types = [
            ColorString(default_value=default_value, allow_none=allow_none),
            RgbTuple(),
            RgbaTuple()
        ]
        super(ColorAlpha, self).__init__(trait_types, **metadata)

    def validate(self, obj, value):
        """
        Verifies that 'value' is a string or tuple and converts it to a
        value like 'rgb(x,y,z)'
        """
        value = super(ColorAlpha, self).validate(obj, value)
        if isinstance(value, tuple):
            if len(value) == 3:
                # convert to an rgb string
                return "rgb({},{},{})".format(*value)
            else:
                # convert to an rgba string
                return "rgba({},{},{},{})".format(*value)
        else:
            # already a string
            return value


def is_valid_point(pt):
    latitude, longitude = pt
    return (-90.0 <= latitude <= 90.0) and (-180.0 <= longitude <= 180.0)
