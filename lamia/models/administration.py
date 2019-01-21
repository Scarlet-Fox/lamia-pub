from .. import db


class Emoji(db.Model):
    __tablename__ = 'emojis'


class Setting(db.Model):
    __tablename__ = 'settings'
    
    
class InstanceBlock(db.Model):
    __tablename__ = 'instance_blocks'

    
class InstanceMute(db.Model):
    __tablename__ = 'instance_mutes'

    
class InstanceCensor(db.Model):
    __tablename__ = 'instance_censors'
        

# TODO: relay support   
#class Relay(db.Model):
#    __tablename__ = 'relays'
