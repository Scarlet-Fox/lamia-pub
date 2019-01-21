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
    
    
class Report(db.Model):
    """Reports are a necessary part of any online social environment. They are
    a way to flag local content for moderators on a local instance, and they 
    can be created and sent to this instance from other instances.  
    """
    __tablename__ = 'reports'
    
class ActorBlock(db.Model):
    __tablename__ = 'actor_blocks'
    
    
    
class ActorMute(db.Model):
    __tablename__ = 'actor_mutes'
    
    
class ActorCensor(db.Model):
    __tablename__ = 'actor_censors'


class DomainBlock(db.Model):
    __tablename__ = 'domain_blocks'
    

class DomainMute(db.Model):
    __tablename__ = 'domain_mutes'
    
    
class DomainCensor(db.Model):
    __tablename__ = 'domain_censors'
    

class DomainEmailBlock(db.Model):
    __tablename__ = 'domain_email_block'
    
    