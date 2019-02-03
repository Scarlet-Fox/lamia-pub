"""This module stores the @context data that will be applied to our internal
lamia objects (and included when they get federated)."""

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
