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
    # the id for an activity is just a uri that can be used to access it
    'id': Field((str, ), True, None),
    # what type of activity is this? there are way too many
    'type': Field((str, ), True, None),
    # what actor is associated with this activity
    'actor': Field((str, ), True, None),
    # when was this activity made available for federation?
    'published': Field((str, ), True,
                       None),  # actually a time in iso8601 format
    # is there an object associated with this activity?
    'object': Field((str, dict), False, None),
    # lists of actors/collections that should receive this object
    'to': Field((list, str), False, None),
    'cc': Field((list, str), False, None),
}

OBJECT_FIELDS = {
    # in most cases, the id and url should be same or similar
    # since the id is a uri where this object lives
    'id': Field((str, ), True, None),
    # what type of object is this? Article/Note/Tombstone/Event
    'type': Field((str, ), True, None),
    # a static url for this object
    'url': Field((str, ), True, None),
    # when was this object made available for federation?
    'published': Field((str, ), True,
                       None),  # actually a time in iso8601 format
    # lists of actors/collections that should receive this object
    'to': Field((list, str), False, None),
    'cc': Field((list, str), False, None),
    # the text content for this object
    'content': Field((str, ), False, None),
    # can contain a list of all replies to this object
    'replies': Field((list, ), False, None),
    # is this a reply? if so, then to what object
    'inReplyTo': Field((str, ), False, None),
    # a summary for the object if it is hidden
    'summary': Field((str, ), False, None),
    # whether or not this object should be cw'd
    'sensitive': Field((bool, ), False, None),
    # attachments listed out email style
    'attachment': Field((list, ), False, None),
    # hashtags associated with this object
    'tag': Field((list, ), False, None),
    # a dictionary mapping iso language codes to content
    'contentMap': Field((dict, ), False, None),
    # who wrote/created this object
    'attributedTo': Field((str, list), False, None),
}

ACTOR_FIELDS = {
    # the id for an actor is just a uri that can be used to access it
    'id': Field((str, ), True, None),
    # what type of actor is this? Person/Service
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
    # contains the public_key for a user
    'publicKey': Field((dict, ), True, None),
    # the static username used in a handle
    'preferredUsername': Field((str, ), False, None),
    # the text description that appears in this actor's profile
    'summary': Field((str, ), True, None),
    # whether or not this user allows automatic follows
    'manuallyApprovesFollowers': Field((bool, ), False, None),
    # a list of 'attachments', used by mastodon for propertyValues
    'attachment': Field((list, ), False, None),
    # a list of hashtags associated with an actor
    'tag': Field((list, ), False, None),
    # seems to only contain the optional sharedInbox address
    'endpoints': Field((dict, ), False, None),
    # an actor's avatar
    'icon': Field((dict, ), False, None),
    # an actor's header
    'image': Field((dict, ), False, None),
}
