from .. import db


class Account(db.Model):
    __tablename__ = 'accounts'
    
    
class Blog(db.Model):
    __tablename__ = 'blogs'
    
    
class Block(db.Model):
    __tablename__ = 'blocks'
    
    
class Mute(db.Model):
    __tablename__ = 'mutes'
    
    
class Filter(db.Model):
    __tablename__ = 'filters'
    
    
class Feed(db.Model):
    __tablename__ = 'feeds'
    
    
class FeedActor(db.Model):
    __tablename__ = 'feed_actors'
    
    
class Follow(db.Model):
    __tablename__ = 'follows'
    
    
class Attachments(db.Model):
    __tablename__ = 'attachments'
    
    
class BookmarkGroup(db.Models):
    __tablename__ = 'bookmark_groups'


class Bookmark(db.Models):
    __tablename__ = 'boookmarks'
    
    