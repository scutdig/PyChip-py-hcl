def signed_num_bin_width(num: int):
    """
    Returns least binary width to hold the specified signed `num`.

    Examples
    --------

    >>> signed_num_bin_width(10)
    5

    >>> signed_num_bin_width(-1)
    2

    >>> signed_num_bin_width(-2)
    3

    >>> signed_num_bin_width(0)
    2
    """

    return len("{:+b}".format(num))


def unsigned_num_bin_width(num: int):
    """
    Returns least binary width to hold the specified unsigned `num`.

    Examples
    --------

    >>> unsigned_num_bin_width(10)
    4

    >>> unsigned_num_bin_width(1)
    1

    >>> unsigned_num_bin_width(0)
    1

    >>> unsigned_num_bin_width(-1)
    Traceback (most recent call last):
    ...
    ValueError: Unexpected negative number: -1
    """

    if num < 0:
        raise ValueError(f"Unexpected negative number: {num}")

    return len("{:b}".format(num))


def get_key_by_value(kvs: dict, value):
    """
    Returns key associated to specified value from dictionary.

    Examples
    --------

    >>> get_key_by_value({1: 'a', 2: 'b'}, 'b')
    2

    >>> get_key_by_value({'a': 1, 'b': 2}, 2)
    'b'

    >>> get_key_by_value({'a': 1, 'b': 1}, 1)
    'a'

    >>> get_key_by_value({1: 'a'}, 'b')
    Traceback (most recent call last):
    ...
    ValueError: b is not in dict values
    """

    vs = list(kvs.values())
    if value not in vs:
        raise ValueError(f"{value} is not in dict values")

    return list(kvs.keys())[vs.index(value)]
