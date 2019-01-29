from gino.dialects.asyncpg import JSONB

from .. import db

# pylint: disable=too-few-public-methods
# Escaping because these are all subclasses


class Emoji(db.Model):
    """A mapping of images, replacement text, and description text all of which
    exists for the purpose of proliferating blob emojis and upside down smiley
    faces throughout the fediverse.
    """
    __tablename__ = 'emojis'

    id = db.Column(db.Integer(), primary_key=True)
    # A path to the image in /statics
    image = db.Column(db.String())
    replacement = db.Column(db.String())
    # Only needed if replacement doesn't do it justice
    description = db.Column(db.String())
    # for linear algebra with emojis, in this essay, i will...
    set_name = db.Column(db.String())


class Setting(db.Model):
    """A basic key and value storage for settings.

    Note: From a philosophical standpoint, settings should all be optional, and
    built around non-essential functionality. The installation of lamia should
    require as little gymnastics as possible and should be, dare I say, Fun.

    TODO: figure out settings we may need here.
    """
    __tablename__ = 'settings'

    id = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String())
    value = db.Column(JSONB())


# TODO: relay support
#class Relay(db.Model):
#    __tablename__ = 'relays'
