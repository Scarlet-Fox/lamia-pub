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


class Activity(db.Model):
    """Activities are things that happen to other things on the fediverse.
    
    From the ActivityPub specifications: 
    * https://www.w3.org/TR/activitypub/#client-to-server-interactions
    * https://www.w3.org/TR/activitypub/#server-to-server-interactions
    """
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer(), primary_key=True)
    
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
    
