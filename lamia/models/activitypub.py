"""Models in this module are directly related to the specifications for 
ActivityPub. They may be referenced by other models but probably shouldn't
depend on them.
"""
from .. import db


class Actor(db.Model):
    """Actually, actors are objects (or ActivityStreams), but I call them out
    explicitly, because they are a key component in how Lamia sees the 
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
    parameters = db.Column(db.JSONB())
    
    display_name = db.Column(db.String())
    uri = db.Column(db.String())
    local = db.Column(db.Boolean())
    
    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())
    
    data = db.Column(db.JSONB())
    
    # Convenience fields for local actors.
    identity_id = db.Column(
        db.Integer(), 
        db.ForeignKey('identities.id', ondelete="SET NULL"),
        nullable=True,
    )
    blog_id = db.Column(
        db.Integer(), 
        db.ForeignKey('blogs.id', ondelete="SET NULL"),
        nullable=True,
    )


class Activity(db.Model):
    """Activities are things that happen to other things on the fediverse.
    
    From the ActivityPub specifications: 
    * https://www.w3.org/TR/activitypub/#client-to-server-interactions
    * https://www.w3.org/TR/activitypub/#server-to-server-interactions
    """
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer(), primary_key=True)
    object_uri = db.Column(db.String())
    
    datetime = db.Column(db.DateTime())
    data = db.Column(db.JSONB())
    
    
class Object(db.Model):
    """Objects are the Things in the fediverse.
    
    From the ActivityPub specifications: 
    https://www.w3.org/TR/activitypub/#obj
    """
    __tablename__ = 'objects'
    
    id = db.Column(db.Integer(), primary_key=True)
    uri = db.Column(db.String())

    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())
    
    data = db.Column(db.JSONB())
    

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
        db.ForeignKey('actors.id', ondelete="CASCADE"),
    )
    target_actor_id = db.Column(
        db.Integer(), 
        db.ForeignKey('actors.id', ondelete="CASCADE"),
    )
    
    # Waiting for account review
    pending_review = db.Column(db.Boolean())
    # Approved by actor owner
    approved = db.Column(db.Boolean())
    # Hard rejected by owner, all future requests will also be blocked
    blocked = db.Column(db.Boolean())
    
    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())