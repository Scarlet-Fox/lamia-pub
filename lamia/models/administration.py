from .. import db




class Emoji(db.Model):
    __tablename__ = 'emojis'


class Setting(db.Model):
    __tablename__ = 'settings'


# TODO: relay support   
#class Relay(db.Model):
#    __tablename__ = 'relays'
