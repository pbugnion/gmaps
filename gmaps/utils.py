
import re

dim_regexp_no_unit = re.compile(r"^\d+$")
dim_regexp = re.compile(r"^(\d+)\s*([a-zA-Z]{2})$")

def parse_css_dimension(value):
    """
    Convert 'value' to a valid CSS dimension.

    Takes its argument and transforms it into a string the CSS parser will
    understand. If units

    """
    if isinstance(value, int):
        v = str(value)
        v += "px"
        return v
    else:
        value = value.strip()
        match_object_no_unit = dim_regexp_no_unit.match(value)
        if match_object_no_unit is None:
            match_object_with_unit = dim_regexp.match(value)
            if match_object_with_unit is None:
                raise ValueError("Dimensions must be of the form ['700', '700px', '7em']. The unit can be"
                        " any valid CSS unit. Received: {}".format(value))
            else:
                value = match_object_with_unit.group(1)
                unit = match_object_with_unit.group(2)
                return value + unit
        return value + "px"

