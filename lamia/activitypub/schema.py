"""Contains functions, classes, convenience methods, and constants that
are used by lamia for manipulating ActivityPub JSON LD representations.

While we could just sling JSON around wildly, this module takes a different
approach and is based on the idea of tightly represented, standardized
JSON formats.

The reason for doing things in this way is to decrease the probability
that a lamia installation becomes a bad neighbor due to garbage data flowing
through the fediverse.
"""
import ujson as json
from lamia.activitypub.fields import FIELD_TYPE, FIELD_REQUIRED, FIELD_VALIDATION


class Schema:
    """The base class for all of our JSON schemata (what a lovely word)."""

    def __init__(self, schema_json: dict = None, fields: dict = None) -> None:
        if schema_json:
            self.representation = schema_json
        else:
            self.representation = {}

        self.fields = fields

    def validate(self) -> bool:
        """Validate the internal JSON representation.

        Returns True if valid. Otherwise, returns False.
        """
        for field, meta in self.fields.items():
            # Does our internal representation contain this key
            field_in_representation = field in self.representation

            # If we should have a field but we do not, then return false
            if meta[FIELD_REQUIRED] and not field_in_representation:
                return False

            if field_in_representation:
                # Is the internal value a valid type? If not, return false
                local_value = self.representation[field]

                valid_type = False
                for _type in meta[FIELD_TYPE]:
                    valid_type = isinstance(local_value, _type)
                    if valid_type:
                        break

                if not valid_type:
                    return False

            return True