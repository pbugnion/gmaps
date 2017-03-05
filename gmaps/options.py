
import collections

from six import string_types


def merge_option_dicts(option_dicts):
    """
    Create a list of options for marker and symbol layers

    This helper function takes a dictionary of (key -> list) and
    returns a list of dictionaries of (key -> value).
    """
    option_values_lengths = [
        len(option_values) for option_values in option_dicts.values()
    ]
    # assert all the list values are the same length
    number_items = option_values_lengths[0]
    assert all(
        length == number_items
        for length in option_values_lengths
    )
    option_lists = []
    for item in range(number_items):
        item_options = {
            option_name: option_values[item]
            for (option_name, option_values)
            in option_dicts.items()
        }
        option_lists.append(item_options)
    return option_lists


def is_atomic(elem):
    """
    True if an element is a single atom and false if it's a collection
    """
    return (
        isinstance(elem, string_types) or
        not isinstance(elem, collections.Iterable)
    )


def is_color_atomic(color):
    """
    Determine whether the argument is a singe color or an iterable of colors
    """
    if isinstance(color, string_types):
        is_atomic = True
    elif isinstance(color, collections.Sequence):
        if isinstance(color[0], string_types):
            is_atomic = False
        elif isinstance(color[0], (int, float)) and len(color) in (3, 4):
            is_atomic = True
        else:
            is_atomic = False
    else:
        is_atomic = True
    return is_atomic


def broadcast_if_atomic(elem, number_elements):
    return [elem] * number_elements if is_atomic(elem) else elem


def broadcast_if_color_atomic(elem, number_elements):
    return [elem] * number_elements if is_color_atomic(elem) else elem
