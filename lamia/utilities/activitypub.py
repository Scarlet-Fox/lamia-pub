"""Contains functions, classes, convenience methods, and constants that
are used by lamia for manipulating ActivityPub JSON LD representations.
"""
from collections import namedtuple
import ujson as json

# In a json-ld world, the @context dictates the shared language between
# lamia and other activitypub implementations.
LAMIA_CONTEXT = [
    # We primarily speak the language of activitystreams
    'https://www.w3.org/ns/activitystreams',
    # For our public key vocabulary
    'https://w3id.org/security/',
    {
        # Extensions from the ActivityStreams namespace
        # https://www.w3.org/wiki/Activity_Streams_extensions
        #   The venerable hashtag, keeper of secrets
        #   a subclass of ActivityPub Object
        'Hashtag': 'as:Hashtag',
        #   Marked as sensitive - content is viewed at user discretion
        'sensitive': 'as:sensitive',
        #   When set to true means that an actor manually approves followers
        #   (considered to convey no meaning when set to False)
        'manuallyApprovesFollowers': 'as:manuallyApprovesFollowers',
        # We will be using the "toot" namespace
        # For a few mastodon specific terms that are Good Ideas
        'toot': 'http://joinmastodon.org/ns#',
        #   If an image should center on a point, this is that point
        #   [X%, Y%] is the format I think, optional for attachments
        'focalPoint': {
            '@container': '@list',
            '@id': 'toot:focalPoint',
        },
        #   A link to a collection of pinned messages on an actor
        'featured': {
            '@id': 'toot:featured',
            '@type': '@id',
        },
        #   Haven't actually come across this in the wild, yet, so I don't
        #   know exactly what it is for, but just stubbing this here to
        #   keep it on the radar
        #   'Emoji': 'toot:Emoji'
        # We will be using the PropertyValue vocabulary for the actor
        # properties displayed as key-value pairs
        'schema': 'http://schema.org#',
        #   Example of Usage (as attachment)
        #   {
        #       "type": "PropertyValue",
        #       "name": "Pronouns",
        #       "value": "they/them"
        #   }
        'PropertyValue': 'schema:PropertyValue',
        'value': 'schema:value'
    }
]
"""For the purpose of clarity and some sanity in a wild world of JSON, we will
use this named tuple set to provide meta data on the basic fields that provide
a satisfactory representation of the data type.

type - a tuple of classes representing (in order of preference) the expected
    field type(s)
required - a booleon variable indicating that this field is not optional
validation - a lamda or other callable usable for field validation

We're using this here to make our handling of JSON a little bit more explicit.

Adding constants here as well, because index lookup is faster than named
fields.
"""
Field = namedtuple('RequireField', 'type required validation')
FIELD_TYPE = 0
FIELD_REQUIRED = 1
FIELD_VALIDATION = 2

# Yes, an activity is actually a subtype of object, but in a world where
# we need to speak to other mastodon-compatible implementations, there are
# some distinct elements of an activity vs an ordinary object.
ACTIVTY_FIELDS = {
    'id': Field((str, ), True, None),
    'type': Field((str, ), True, None),
    'actor': Field((str, ), True, None),
    'published': Field((str, ), True,
                       None),  # actually a time in iso8601 format
    'object': Field((str, dict), False, None),
    'to': Field((list, str), False, None),
    'cc': Field((list, str), False, None),
}

OBJECT_FIELDS = {
    'id': Field((str, ), True, None),
    'type': Field((str, ), True, None),
    'url': Field((str, ), True, None),
    'published': Field((str, ), True,
                       None),  # actually a time in iso8601 format
    'to': Field((list, str), False, None),
    'cc': Field((list, str), False, None),
    'content': Field((str, ), False, None),
    'inReplyTo': Field((str, ), False, None),
    'summary': Field((str, ), False, None),
    'sensitive': Field((bool, ), False, None),
    'attachment': Field((list, ), False, None),
    'tag': Field((list, ), False, None),
    'contentMap': Field((dict, ), False, None),
    'attributedTo': Field((str, list), False, None),
}

ACTOR_FIELDS = {
    'id': Field((str, ), True, None),
    'type': Field((str, ), True, None),
    # a static url for this actor
    'url': Field((str, ), True, None),
    # urls for collections of followers and following
    'followers': Field((str, ), True, None),
    'following': Field((str, ), True, None),
    # POSTable url for sending mail^H^H^H^H activities to this actor
    'inbox': Field((str, ), True, None),
    # GETable url for a collection of this actor's activities
    'outbox': Field((str, ), True, None),
    # a url for a collection of pinned objects
    'featured': Field((str, ), False, None),
    # the display name associated with an actor
    'name': Field((str, ), True, None),
    'publicKey': Field((dict, ), True, None),
    # the static username used in a handle
    'preferredUsername': Field((str, ), False, None),
    # the text description that appears in this actor's profile
    'summary': Field((str, ), True, None),
    # whether or not this user allows automatic follows
    'manuallyApprovesFollowers': Field((bool, ), False, None),
    'attachment': Field((list, ), False, None),
    'tag': Field((list, ), False, None),
    'endpoints': Field((dict, ), False, None),
    'icon': Field((dict, ), False, None),
    'image': Field((dict, ), False, None),
}
