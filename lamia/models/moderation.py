from .. import db


class Import(db.Model):
    __tablename__ = 'imports'
    
    
class Report(db.Model):
    __tablename__ = 'reports'
    
    
# Moderators determined by flags on accounts

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
    
    