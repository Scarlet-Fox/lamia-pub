"""Models in this module are directly related to the specifications for
ActivityPub. They may be referenced by other models but probably shouldn't
depend on them.
"""
from gino.dialects.asyncpg import JSONB
from lamia.database import db


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
    actor_type = db.Column(db.String())
    private_key = db.Column(db.String(), nullable=True)

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
        db.ForeignKey('identities.id', ondelete='SET NULL',name='fk_actor_identity'),
        nullable=True
    )
    blog_id = db.Column(
        db.Integer(),
        db.ForeignKey('blogs.id', ondelete='SET NULL',name='fk_actor_blog'),
        nullable=True
    )


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
        db.ForeignKey('actors.id', ondelete='SET NULL', name='fk_object_created_by_actor'),
        nullable=True,
    )
    last_updated = db.Column(db.DateTime())

    data = db.Column(JSONB())
