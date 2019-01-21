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


class Activity(db.Model):
    """Activities are things that happen to other things on the fediverse.
    
    From the ActivityPub specifications: 
    * https://www.w3.org/TR/activitypub/#client-to-server-interactions
    * https://www.w3.org/TR/activitypub/#server-to-server-interactions
    """
    __tablename__ = 'activities'
    
    
class Object(db.Model):
    """Objects are the Things in the fediverse.
    
    From the ActivityPub specifications: 
    https://www.w3.org/TR/activitypub/#obj
    """
    __tablename__ = 'objects'
    
    
