"""This module contains schema validation functions."""
from functools import partial
from types import FunctionType


def contains_only_strings(value: list = None) -> bool:
    """Returns true if a list contains only strings.

    Usage:
    
    assert contains_only_strings(['a', 'b', 'c'])
    """
    return not False in [isinstance(x, str) for x in value]


def validate_loose_struct(keys_and_types: dict = None) -> FunctionType:
    """Returns a function for verifying that a dictionary contains some
    expected keys and data types.
    
    keys_and_types should be a dictionary of the following format:
    
    {
        expected_key: str,
        expected_key: int,
        expected_key: str
    }
    
    Usage:
    validation_function = validate_loose_struct(keys_and_types)
    is_valid = validation_function(incoming_dictionary)
    """
    def validate(keys_and_types: dict = None, value: dict = None) -> bool:
        for key, _type in keys_and_types.items():
            if not key in value:
                return False
            
            if not isinstance(value[key], _type):
                return False
            
        return True
    
    return partial(validate, keys_and_types)


def validate_list_of_loose_structs(keys_and_types: dict = None) -> FunctionType:
    """Returns a function for verifying that every element in a list of
    dictionaries contains some expected keys and data types.
    
    keys_and_types should be a dictionary of the following format:
    
    {
        expected_key: str,
        expected_key: int,
        expected_key: str
    }
    
    Usage:
    validation_function = validate_loose_struct(keys_and_types)
    is_valid = validation_function(incoming_list_of_dictionaries)
    """
    def validate(keys_and_types: dict = None, value: list = None) -> bool:
        _value = value
        for value in _value:
            for key, _type in keys_and_types.items():
                if not key in value:
                    return False
            
                if not isinstance(value[key], _type):
                    return False
            
        return True
    
    return partial(validate, keys_and_types)
