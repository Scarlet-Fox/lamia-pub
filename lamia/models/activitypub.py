"""Models in this module are directly related to the specifications for
ActivityPub. They may be referenced by other models but probably shouldn't
depend on them.


"""
import pendulum
from gino.dialects.asyncpg import JSONB
from .. import db

# pylint: disable=too-few-public-methods
# Escaping because these are all subclasses

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


class Actor(db.Model):
    """Actually, actors are objects (or ActivityStreams), but I call them out
    explicitly, because they are a key component in how lamia sees the
    fediverse.

    From the ActivityPub specifications:
    https://www.w3.org/TR/activitypub/#actors

    All the world’s a stage,
    And all the identities and blogs merely actors
    - Snakespeare, As You Lamia It
    """
    __tablename__ = 'actors'

    id = db.Column(db.Integer(), primary_key=True)

    avatar = db.Column(db.String())
    header = db.Column(db.String())
    summary = db.Column(db.String())
    actor_type = db.Column(db.String())
    private_key = db.Column(db.String())

    display_name = db.Column(db.String())
    user_name = db.Column(db.String())
    uri = db.Column(db.String())
    local = db.Column(db.Boolean())

    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())

    data = db.Column(JSONB())

    # Convenience fields for local actors.
    identity_id = db.Column(
        db.Integer(),
        db.ForeignKey('identities.id', ondelete='SET NULL'),
        nullable=True,
    )
    blog_id = db.Column(
        db.Integer(),
        db.ForeignKey('blogs.id', ondelete='SET NULL'),
        nullable=True,
    )

    def build_from_json(self, json_ld, local=False):
        """Receives a python dict and then populates the other fields in the
        model; with the goal being to be ready to saving to the database.
        """
        self.avatar = json_ld['icon']['url']
        self.header = json_ld['image']['url']
        self.summary = json_ld['summary']
        self.display_name = json_ld['name']
        self.uri = json_ld['id']
        self.actor_type = json_ld['type']
        self.user_name = json_ld['preferredUsername']
        self.local = local
        self.created = pendulum.now()
        self.last_updated = pendulum.now()
        self.data = json_ld

    def build_from_params(
            self,
            public_key,
            key_id,
            key_owner,
            _id,
            _type,
            following,
            followers,
            inbox,
            outbox,
            user_name,
            display_name,
            summary,
            url,
            local=False,
            private_key='',
            avatar={},
            header={},
            endpoints={},
            attachment=[],
            tag=[],
            featured=[],
            manually_approves=False,
    ):
        """Receives a number of parameters and populates the internal fields in
        this models; with the goal being to be ready to saving to the database.
        """

        data = {
            'id': _id,
            'type': _type,
            'following': following,
            'followers': followers,
            'inbox': inbox,
            'outbox': outbox,
            'featured': featured,
            'preferredUsername': user_name,
            'name': display_name,
            'summary': summary,
            'url': url,
            'manuallyApprovesFollowers': manually_approves,
            'publicKey': {
                'id': key_id,
                'owner': key_owner,
                'publicKeyPem': public_key,
            },
            'tag': tag,
            'attachment': attachment,
            'endpoints': endpoints,
            'icon': avatar,
            'image': header,
        }
        self.avatar = avatar['url']
        self.header = header['url']
        self.summary = summary
        self.display_name = display_name
        self.uri = _id
        self.actor_type = _type
        self.user_name = user_name
        self.local = local
        self.created = pendulum.now()
        self.last_updated = pendulum.now()
        self.data = data


class Activity(db.Model):
    """Activities are things that happen to other things on the fediverse.

    From the ActivityPub specifications:
    * https://www.w3.org/TR/activitypub/#client-to-server-interactions
    * https://www.w3.org/TR/activitypub/#server-to-server-interactions
    """
    __tablename__ = 'activities'

    id = db.Column(db.Integer(), primary_key=True)
    uri = db.Column(db.String())
    object_uri = db.Column(db.String())
    actor_uri = db.Column(db.String())
    activity_type = db.Column(db.String())

    created = db.Column(db.DateTime())
    data = db.Column(JSONB())

    def build_from_json(self, json_ld):
        """Receives a python dict and then populates the other fields in the
        model; with the goal being to be ready to saving to the database.
        """
        self.data = json_ld
        self.created = pendulum.parse(json_ld['published'])
        self.uri = json_ld['id']
        self.actor_uri = json_ld['actor']
        self.activity_type = json_ld['type']
        self.last_updated = pendulum.now()

    def build_from_params(self, _id, _type, actor_uri, published, to, cc,
                          _object):
        """Receives a number of parameters and populates the internal fields in
        this models; with the goal being to be ready to saving to the database.
        """

        data = {
            'id': _id,
            'type': _type,
            'actor': actor_uri,
            'published': published,  # Should be a pendulum DateTime
            'to': to,
            'cc': cc,
            'object': _object,
        }
        self.data = data
        self.created = published
        self.uri = json_ld['id']
        self.actor_uri = json_ld['actor']
        self.activity_type = json_ld['type']
        self.last_updated = pendulum.now()


class Object(db.Model):
    """Objects are the Things in the fediverse.

    From the ActivityPub specifications:
    https://www.w3.org/TR/activitypub/#obj
    """
    __tablename__ = 'objects'

    id = db.Column(db.Integer(), primary_key=True)
    uri = db.Column(db.String())
    actor_uri = db.Column(db.String())
    reply_to_uri = db.Column(db.String())
    object_type = db.Column(db.String())

    created = db.Column(db.DateTime())
    created_by_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='SET NULL'),
        nullable=True,
    )
    last_updated = db.Column(db.DateTime())

    data = db.Column(JSONB())

    def build_from_json(self, json_ld):
        """Receives a python dict and then populates the other fields in the
        model; with the goal being to be ready to saving to the database.
        """
        self.data = json_ld
        self.created = pendulum.parse('published')
        self.uri = json_ld['id']
        self.actor_uri = json_ld['attributedTo']
        self.object_type = json_ld['type']
        self.last_updated = pendulum.now()

    def build_from_params(
            self,
            _id,
            _type,
            published,
            url,
            actor,
            to,
            cc,
            content,
            content_map,
            _object,
            attachment=[],
            tag=[],
            summary=None,
            reply_to_uri=None,
            sensitive=False,
    ):
        """Receives a number of parameters and populates the internal fields in
        this models; with the goal being to be ready to saving to the database.
        """

        data = {
            'id': _id,
            'type': _type,
            'published': published,  # Should be a pendulum DateTime
            'url': url,
            'attributedTo': actor,
            'to': to,
            'cc': cc,
            'content': content,
            'contentMap': content_map,
            'attachment': attachment,
            'tag': tag,
            'summary': summary,
            'inReplyTo': reply_to_uri,
            'sensitive': sensitive,
        }
        self.data = data
        self.created = published
        self.uri = _id
        self.actor_uri = actor
        self.object_type = _type
        self.last_updated = pendulum.now()


class Follow(db.Model):
    """Subscriptions are a link between actors. When you subscribe, you are
    saying, "yes, please, show me the things that you create."

    This activity is explicitly supported by ActivityPub, but I call it out
    explicitly for convenience. Explicitly..
    """
    __tablename__ = 'follows'

    id = db.Column(db.Integer(), primary_key=True)
    actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='CASCADE'),
    )
    target_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='CASCADE'),
    )

    # Waiting for account review
    pending_review = db.Column(db.Boolean())
    # Approved by actor owner
    approved = db.Column(db.Boolean())
    # Hard rejected by owner, all future requests will also be blocked
    blocked = db.Column(db.Boolean())

    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())
