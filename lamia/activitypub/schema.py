"""Contains functions, classes, convenience methods, and constants that
are used by lamia for manipulating ActivityPub JSON LD representations.

While we could just sling JSON around wildly, this module takes a different
approach and is based on the idea of tightly represented, standardized
JSON formats.

The reason for doing things in this way is to decrease the probability
that a lamia installation becomes a bad neighbor due to garbage data flowing
through the fediverse.

Note: These classes speak JSON but they do so in the form of a Python
dictionary.
"""
import logging
from typing import Any
from lamia.activitypub.fields import FIELD_TYPE, FIELD_REQUIRED, FIELD_VALIDATION
from lamia.activitypub.fields import ACTIVTY_FIELDS, OBJECT_FIELDS, ACTOR_FIELDS
from lamia.activitypub.context import LAMIA_CONTEXT
LOGGER = logging.getLogger('lamia')


class SchemaValidationException(Exception):
    """Schema validation exceptions are raised when a schema is badly formed
    in accordance with the given meta data..
    """


class Schema:
    """The base class for all of our JSON schemata (what a lovely word)."""

    def __setattr__(self, name: str, value: Any) -> None:
        """We overrride python's standard attribute setting method to provide
        a prettier way to access the internal representation than accessing
        the dictionary directly.

        A benefit to taking this approach is that it allows for inline
        validation of values that are being set.
        """

        # Only fields and representation are set directly everything
        # else is assumed to be in the internal json ld representation.
        if name in ('fields', 'representation'):
            object.__setattr__(self, name, value)
        else:
            if self.validate_field(name, value):
                self.representation[name] = value
            else:
                raise SchemaValidationException(
                    f'invalid value {value} for {name}')

    def __getattr__(self, name: str) -> Any:
        return self.representation[name]

    def __init__(self, json_to_load: dict, fields: dict = None) -> None:
        """Setup the internal object."""

        if json_to_load:
            self.representation = json_to_load
        else:
            self.representation = {}

        self.fields = fields

    def load_json_ld(self, json_to_load: dict = None) -> None:
        """A convenience method for loading the internal dictionary.

        This may be replaced by something more durable later on.
        """
        self.representation = json_to_load

    def to_json_ld(self) -> dict:
        """Returns a copy of the representation as it is."""
        return self.representation.copy()

    def to_lamia_json_ld(self) -> None:
        """Adds lamia's context to a copy of the representation and then
        returns.
        """

        json_ld = self.representation.copy()
        json_ld['@context'] = LAMIA_CONTEXT
        return json_ld

    def validate_field(self, field: str, value_to_test: Any = None) -> bool:
        """If given a field name, this function verifies either the existing
        internal value or the given value_to_test.

        It returns True when a field is Not Invalidated. This means that a
        True return value is expected when a field doesn't exist yet and isn't
        required (because a non-existant field can't invalidate).
        """
        # Does our internal representation contain this key
        field_in_representation = field in self.representation

        # If this field is not part of our fields metadata, allow it
        try:
            meta = self.fields[field]
        except KeyError:
            return True

        # If we are performing a theoretical test, don't expect the field
        # to have already been in the internal representation.
        if value_to_test is None:
            # If we should have a field but we do not, then return false
            if meta[FIELD_REQUIRED] and not field_in_representation:
                LOGGER.warning(f'required field {field} is not in schema')
                return False

        # Set the local value to either the given value or the existing
        # internal value.
        if value_to_test is None:
            # If we are validating a field that is in the fields metadata
            # then set it if it exists, if it does not exist, then return
            # true because it is not invalidating any tests if it doesn't
            # exist.
            try:
                local_value = self.representation[field]
            except KeyError:
                return True
        else:
            local_value = value_to_test

        # Is the local value a valid type? If not, return false
        valid_type = False
        type_idx = None
        for i, _type in enumerate(meta[FIELD_TYPE]):
            valid_type = isinstance(local_value, _type)

            if valid_type:
                type_idx = i
                break

        if not valid_type:
            LOGGER.warning(f'field {field} is not a valid type in schema')
            return False

        # Check the validation function associated with the type
        validation_function = meta[FIELD_VALIDATION][type_idx]

        if validation_function:
            if not validation_function(local_value):
                LOGGER.warning(f'field {field} failed validation in schema')
                return False

        return True

    def validate(self) -> bool:
        """Validate the internal JSON representation.

        Returns True if valid. Otherwise, returns False.
        """
        for field in self.fields.keys():
            if not self.validate_field(field):
                return False

        return True


class PubActivity(Schema):
    """A schema representing an activitypub activity."""

    def __init__(self, json_to_load: dict = None) -> None:
        super().__init__(fields=ACTIVTY_FIELDS, json_to_load=json_to_load)


class PubObject(Schema):
    """A schema representing an activitypub object."""

    def __init__(self, json_to_load: dict = None) -> None:
        super().__init__(fields=OBJECT_FIELDS, json_to_load=json_to_load)


class PubActor(Schema):
    """A schema representing an activitypub actor."""

    def add_property(self, name: str = None, value: str = None) -> None:
        """A convenience method for adding a property to an actor."""
        if 'attachments' not in self.representation:
            self.representation['attachments'] = []

        property_entry = {
            'type': 'PropertyValue',
            'name': name,
            'value': value,
        }

        self.representation['attachments'].append(property_entry)

    def del_property(self, idx: int = None) -> None:
        """A convenience method for removing a property from an actor."""
        if 'attachments' not in self.representation:
            return

        del self.representation['attachments'][idx]

    def __init__(self, json_to_load: dict = None) -> None:
        super().__init__(fields=ACTOR_FIELDS, json_to_load=json_to_load)
