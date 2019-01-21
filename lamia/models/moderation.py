"""Models that pertain directly to the messy business of keeping an online 
environment safe from harmful intentions are in this module.
"""
from .. import db


class Import(db.Model):
    """Followed, muted, and blocked actors can be imported from ActivityPub 
    files. 
    
    These imports should not run automatically because of the potential 
    for abuse, particularly from "follow" actions. Instead, they are stored here 
    and can be selectively authorized to move forward by moderators.
    """
    __tablename__ = 'imports'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Report(db.Model):
    """Reports are a necessary part of any online social environment. They are 
    a way to flag local content for moderators on a local instance, and they 
    can be created and sent to this instance from other instances. 
    """
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
class ActorCensor(db.Model):
    """An actor censor is a light server to client moderation action.
    
    An actor censor is a created at the server level, and forces an actors' 
    activities to either appear content warned or minimized.
    """
    __tablename__ = 'actor_censors'
    
    id = db.Column(db.Integer(), primary_key=True)
    


class ActorMute(db.Model):
    """An actor block is a moderate server to client moderation action.
    
    An actor mute is a created at the server level, and either hides the actor's
    activities from the federated timeline or minimizes them.
    """
    __tablename__ = 'actor_mutes'
    
    id = db.Column(db.Integer(), primary_key=True)
    


class ActorBlock(db.Model):
    """An actor block is a severe server to client moderation action.
    
    An actor block is a created at the server level, and probits the blocked 
    actor from interacting with the instance. It also breaks follows between 
    actors on this instance and the actor that is blocked.
    """
    __tablename__ = 'actor_blocks'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class DomainCensor(db.Model):
    """A domain censor is a light server to server moderation action. 
    
    An domain censor is a created at the server level, and forces all activities
    from a specific domain to either appear content warned or minimized.
    """
    __tablename__ = 'domain_censors'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class DomainMute(db.Model):
    """A domain mute is a moderate server to server moderation action. 
    
    A domain mute is a created at the server level, and either hides the domains'
    activities from the federated timeline or minimizes them.
    """
    __tablename__ = 'domain_mutes'
    
    id = db.Column(db.Integer(), primary_key=True)
    


class DomainBlock(db.Model):
    """A domain block is a severe server to client moderation action.
    
    A domain block is a created at the server level, and probits all actors on
    a blocked instance from interacting with the local instance. It also breaks 
    follows between actors on this instance and the instance that is blocked.
    """
    __tablename__ = 'domain_blocks'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    

class DomainEmailBlock(db.Model):
    """Email domain blocks prevent harmful registrations and registrations 
    from spammers.
    """
    __tablename__ = 'domain_email_block'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    