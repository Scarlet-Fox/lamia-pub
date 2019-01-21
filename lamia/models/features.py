"""Models in this module are the sugar that makes Lamia worth using over
just a plain federator. They're directly or indirectly associated with the
user-level things that make ActivityPub taste better.
"""
from .. import db


class Account(db.Model):
    """Login details for user actors are stored here. Accounts in lamia are 
    best explained as being containers for blogs and identities, where both of
    these are 1-to-1 connections to ActivityPub actors.
    
    Basically, an account on lamia can own multiple identities and blogs. These 
    identities and blogs are what others see when someone with an account makes
    a post.
    
    TODO: to prevent intentional/unintentional abuse, this needs to be VERY
    transparent.
    """
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Identity(db.Model):
    """An account can have more than one identity. Each identity connects an 
    account to a single ActivityPub actor.
    """
    __tablename__ = 'identities'
    
    id = db.Column(db.Integer(), primary_key=True)
    

    
class Blog(db.Model):
    """An account can have more than one blog. Each blog connects an 
    account to a single ActivityPub actor.
    """
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Block(db.Model):
    """Blocking a user is the strongest user to user moderation action.
    
    It's a way of saying, "remove all of this user's stuff from my sight."
    
    Blocking a user prevents all interaction between the users, breaks follows,
    and more or less cleanses the timeline of that user.
    
    Blocks are officially a part of the ActivityPub specification, but I am
    calling them out explicitly with a seperate model for consistency.
    """
    __tablename__ = 'blocks'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Mute(db.Model):
    """Muting a user is a lightweight user to user moderation action.
    
    It's a way of saying, "you're a bit much. i need some space." This can be a
    temporary mute, for example, just for a moment to allow someone else to
    cool down.
    
    Muting a user silences notifications, maintains follows, and either 
    squelches them from timelines or minimizes them.
    """
    __tablename__ = 'mutes'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Filter(db.Model):
    """Filters are best described as a more nuanced version of muting, allowing
    specific words to be removed from a timeline or minimized within the 
    timeline.
    """
    __tablename__ = 'filters'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Feed(db.Model):
    """A feed is a set of actors that you want to create a custom timeline
    for. As an example, you could create a feed labeled "friends" for calling
    out your friends' blog posts and statuses.
    
    It's worth noting that you need to subscribe to an actor before this works.
    """
    __tablename__ = 'feeds'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class FeedActor(db.Model):
    """A single actor watched by a feed."""
    __tablename__ = 'feed_actors'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Follow(db.Model):
    """Subscriptions are a link between actors. When you subscribe, you are
    saying, "yes, please, show me the things that you create."
    
    This activity is explicitly supported by ActivityPub, but I call it out 
    explicitly for convenience.
    """
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class Attachments(db.Model):
    """An attachment is an image tied to some kind of ActivityPub object.
    
    TODO: We can look into non-image attachments and probably dismiss the
    possibility of them later on.
    """
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer(), primary_key=True)
    
    
    
class BookmarkGroup(db.Models):
    """Bookmark groups can be implicitly created to organize bookmarks"""
    __tablename__ = 'bookmark_groups'
    
    id = db.Column(db.Integer(), primary_key=True)
    


class Bookmark(db.Models):
    """A bookmark is a "saved" link to an ActivityPub object that is not
    an actor."""
    __tablename__ = 'boookmarks'
    
    id = db.Column(db.Integer(), primary_key=True)
    