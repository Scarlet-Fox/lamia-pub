import pytest
# Import lamia either from pythonpath or a relative parent dir
try:
    import lamia
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())

from lamia.activitypub.schema import ACTIVTY_FIELDS, OBJECT_FIELDS, ACTOR_FIELDS


def test_field_definitions():
    def check_tuples(fieldset):
        for field, meta in fieldset.items():
            assert len(meta.type) == len(meta.validation)
            
    check_tuples(ACTIVTY_FIELDS)
    check_tuples(OBJECT_FIELDS)
    check_tuples(ACTOR_FIELDS)


