
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
