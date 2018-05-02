
import re

import traitlets

from .locations import locations_to_list


class InvalidPointException(Exception):
    pass


class InvalidWeightException(Exception):
    pass


class LocationArray(traitlets.List):
    info_text = 'An iterable of locations'
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        if value is None:
            return super(LocationArray, self).validate(obj, value)
        locations_as_list = locations_to_list(value)
        for location in locations_as_list:
            latitude, longitude = location
            _validate_latitude(latitude)
            _validate_longitude(longitude)
        return super(LocationArray, self).validate(obj, locations_as_list)


class WeightArray(traitlets.List):
    info_text = 'An iterable of non-negative weights'
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        if value is None:
            return super(WeightArray, self).validate(obj, value)
        weights = list(value)
        for weight in weights:
            try:
                weight = float(weight)
            except (TypeError, ValueError):
                raise traitlets.TraitError(
                    '{} is not a valid weight. '
                    'Weights must be floats'.format(weight)
                )
            if weight < 0.0:
                raise InvalidWeightException(
                    '{} is not a valid weight. '
                    'Weights must be non-negative.'.format(weight)
                )
        return super(WeightArray, self).validate(obj, weights)


class Latitude(traitlets.Float):
    """
    Float representing a latitude

    Latitude values must be between -90 and 90.
    """
    info_text = 'a valid latitude (-90 <= latitude <= 90)'
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        _validate_latitude(value)
        return value


class Longitude(traitlets.Float):
    """
    Float representing a longitude

    Longitude values must be between -180 and 180.
    """
    info_text = 'a valid longitude (-180 <= longitude <= 180)'
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        _validate_longitude(value)
        return value


class Point(traitlets.Tuple):
    """
    Tuple representing a (latitude, longitude) pair.
    """
    info_text = 'a valid (latitude, longitude) pair'

    def __init__(self, default_value=traitlets.Undefined):
        super(Point, self).__init__(
            Latitude(), Longitude(), default_value=default_value)

    def validate(self, obj, value):
        if value is not None:
            if len(value) != 2:
                raise traitlets.TraitError(
                    '{} is not a valid location. '
                    'Locations must have length 2.'.format(value)
                )
            latitude, longitude = value
            return super(Point, self).validate(obj, (latitude, longitude))


_color_names = {
    'black', 'silver', 'gray', 'white', 'maroon', 'red',
    'purple', 'fuschia', 'green', 'lime', 'olive',
    'yellow', 'navy', 'blue', 'teal', 'aqua'
}

_color_re = re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$')
_rgb_re = re.compile(r'rgb\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3}\)')
_rgba_re = re.compile(
    r'rgba\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3},(?:0?\.[0-9]*|1\.0|1|0)\)'
)


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
            normalised_string = value_as_string.replace(' ', '').lower()
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
    info_text = 'a triple of integers between 0 and 255 like (100, 0, 250)'

    def __init__(self, **metadata):
        traits = [
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255)
        ]
        super(RgbTuple, self).__init__(*traits, **metadata)


class RgbaTuple(traitlets.Tuple):
    info_text = 'an RGBA tuple like (100, 0, 250, 0.5)'

    def __init__(self, **metadata):
        traits = [
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Int(traitlets.Undefined, min=0, max=255),
            traitlets.Float(traitlets.Undefined, min=0.0, max=1.0)
        ]
        super(RgbaTuple, self).__init__(*traits, **metadata)


class ZoomLevel(traitlets.Integer):
    """
    Integer representing a zoom value allowed by Google Maps
    """
    info_text = 'a valid Google Maps zoom (0 <= zoom <= 21)'
    default_value = traitlets.Undefined

    def validate(self, obj, value):
        if 0 <= value <= 21:
            return value
        else:
            self.error(obj, value)


class Tilt(traitlets.Integer):
    """
    Integer representing a tilt degree allowed by Google Maps
    """
    info_text = 'tilt angle in degrees (either 0 or 45)'
    default_value = 45

    def validate(self, obj, value):
        if value in {0, 45}:
            return value
        else:
            self.error(obj, value)


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
                return 'rgb({},{},{})'.format(*value)
            else:
                # convert to an rgba string
                return 'rgba({},{},{},{})'.format(*value)
        else:
            # already a string
            return value


class MapType(traitlets.Enum):
    """
    String representing a map type
    """
    allowed_map_types = ['ROADMAP', 'HYBRID', 'TERRAIN', 'SATELLITE']

    def __init__(self, default_value, **kwargs):
        super(MapType, self).__init__(
            self.allowed_map_types,
            default_value=default_value,
            allow_none=False,
            **kwargs
        )


class MouseHandling(traitlets.Enum):
    """
    String representing valid values for mouse handling
    """
    allowed_behaviours = ['COOPERATIVE', 'GREEDY', 'NONE', 'AUTO']

    def __init__(self, default_value, **kwargs):
        super(MouseHandling, self).__init__(
            self.allowed_behaviours,
            default_value=default_value,
            allow_none=False,
            **kwargs
        )


class Opacity(traitlets.Float):
    info_text = 'a valid opacity value (0.0 <= opacity <= 1.0)'

    def __init__(
            self, default_value=traitlets.Undefined,
            allow_none=False, **kwargs
    ):
        super(Opacity, self).__init__(
            default_value=default_value,
            allow_none=allow_none,
            min=0.0,
            max=1.0,
            **kwargs)


def is_valid_point(pt):
    latitude, longitude = pt
    return (-90.0 <= latitude <= 90.0) and (-180.0 <= longitude <= 180.0)


def _validate_latitude(latitude):
    try:
        latitude = float(latitude)
    except (TypeError, ValueError):
        raise traitlets.TraitError(
            '{} is not a valid latitude. '
            'Latitudes must be floats'.format(latitude)
        )
    if not (-90.0 <= latitude <= 90.0):
        raise InvalidPointException(
            '{} is not a valid latitude. '
            'Latitudes must lie between -90 and 90.'.format(latitude)
        )


def _validate_longitude(longitude):
    try:
        longitude = float(longitude)
    except (TypeError, ValueError):
        raise traitlets.TraitError(
            '{} is not a valid longitude. '
            'Longitudes must be floats'.format(longitude)
        )
    if not (-180.0 <= longitude <= 180.0):
        raise InvalidPointException(
            '{} is not a valid longitude. '
            'Longitudes must lie between '
            '-180 and 180.'.format(longitude)
        )
