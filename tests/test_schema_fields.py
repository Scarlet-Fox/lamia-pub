import sys
import os
sys.path.append(os.getcwd())

import pytest

from lamia.activitypub.fields import ACTIVTY_FIELDS, OBJECT_FIELDS, ACTOR_FIELDS
from lamia.activitypub.validation import contains_only_strings
from lamia.activitypub.validation import validate_loose_struct
from lamia.activitypub.validation import validate_list_of_loose_structs


def test_field_definitions():
    def check_tuples(fieldset):
        for field, meta in fieldset.items():
            assert len(meta.type) == len(meta.validation)
            
    check_tuples(ACTIVTY_FIELDS)
    check_tuples(OBJECT_FIELDS)
    check_tuples(ACTOR_FIELDS)


def test_contains_only_strings_validator():
    assert contains_only_strings(['a', 'b', 'c'])
    assert contains_only_strings(['a', 'b', 1]) == False


def test_validate_loose_struct():
    expected_keys_and_types = {
        'i_expect_a_string': str,
        'i_expect_an_int': int,
    }
    
    good_data = {
        'i_expect_a_string': 'a',
        'i_expect_an_int': 1,
    }
    
    bad_data_type = {
        'i_expect_a_string': 1,
        'i_expect_an_int': 1,
    }
    
    bad_data_keys = {
        'i_expect_an_int': 1,
    }
    
    validation_function = validate_loose_struct(expected_keys_and_types)
    assert validation_function(good_data)
    assert validation_function(bad_data_type) == False
    assert validation_function(bad_data_keys) == False
    
def test_validate_list_of_loose_struct():
    expected_keys_and_types = {
        'i_expect_a_string': str,
        'i_expect_an_int': int,
    }
    
    good_data = [
        {'i_expect_a_string': 'a', 'i_expect_an_int': 1},
        {'i_expect_a_string': 'b', 'i_expect_an_int': 2},
    ]
    
    bad_data_type = [
        {'i_expect_a_string': 'a', 'i_expect_an_int': 1},
        {'i_expect_a_string': 'b', 'i_expect_an_int': 'c'},
    ]
    
    bad_data_keys = [
        {'i_expect_a_string': 'a', 'i_expect_an_int': 1},
        {'i_expect_an_int': 2},
    ]
    
    validation_function = validate_list_of_loose_structs(expected_keys_and_types)
    assert validation_function(good_data)
    assert validation_function(bad_data_type) == False
    assert validation_function(bad_data_keys) == False
    