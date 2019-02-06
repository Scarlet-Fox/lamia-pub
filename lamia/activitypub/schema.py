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
from lamia.activitypub.fields import ACTIVTY_FIELDS, OBJECT_FIELDS, ACTOR_FIELDS


class SchemaValidationError(Exception):
    """Raised when validation fails for a loaded schema."""


class Schema:
    """The base class for all of our JSON schemata (what a lovely word)."""

    def __init__(self, json_to_load: dict = None, fields: dict = None) -> None:
        if json_to_load:
            self.representation = json_to_load
        else:
            self.representation = {}

        self.fields = fields

    def load_json(self, json_to_load: dict = None) -> None:
        """A convenience method for loading the internal dictionary.

        This may be replaced by something more durable later on.
        """
        self.representation = {}

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
                type_idx = None
                for i, _type in enumerate(meta[FIELD_TYPE]):
                    valid_type = isinstance(local_value, _type)

                    if valid_type:
                        type_idx = i
                        break

                if not valid_type:
                    return False

                # Check the validation function associated with the type
                validation_function = meta[FIELD_VALIDATION][type_idx]

                if validation_function:
                    if not validation_function(local_value):
                        return False

        return True


class Activity(Schema):
    """A schema representing an activitypub activity."""
    def __init__(self, json_to_load: dict = None) -> None:
        super().__init__(fields=ACTIVTY_FIELDS, json_to_load=json_to_load)


class Object(Schema):
    """A schema representing an activitypub object."""
    def __init__(self, json_to_load: dict = None) -> None:
        super().__init__(fields=OBJECT_FIELDS, json_to_load=json_to_load)


class Actor(Schema):
    """A schema representing an activitypub actor."""
    def __init__(self, json_to_load: dict = None) -> None:
        super().__init__(fields=ACTOR_FIELDS, json_to_load=json_to_load)

