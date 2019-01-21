from .. import db

class Emoji(db.Model):
    """A mapping of images, replacement text, and description text all of which
    exists for the purpose of proliferating blob emojis and upside down smiley
    faces throughout the fediverse.
    """
    __tablename__ = 'emojis'
    
    id = db.Column(db.Integer(), primary_key=True)
    


class Setting(db.Model):
    """A basic key and value storage for settings.
    
    Note: From a philosophical standpoint, settings should all be optional, and
    built around non-essential functionality. The installation of Lamia should
    require as little gymnastics as possible and should be, dare I say, Fun.
    
    TODO: figure out settings we may need here.
    """
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer(), primary_key=True)
    


# TODO: relay support   
#class Relay(db.Model):
#    __tablename__ = 'relays'
