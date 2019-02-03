"""This module contains schema validation functions."""
from functools import partial
from types import FunctionType


def contains_only_strings(value: list = None) -> bool:
    """Returns true if a list contains only strings.

    Usage:

    assert contains_only_strings(['a', 'b', 'c'])
    """
    return not False in [isinstance(x, str) for x in value]
