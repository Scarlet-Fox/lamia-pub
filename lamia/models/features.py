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
    primary_identity_id = db.Column(db.Column(), db.ForeignKey('identities.id'))
    email_address = db.Column(db.String())
    # Should be a hash encrypted by scrypt
    password = db.Column(db.String())
    joined = db.Column(db.DateTime())
    low_bandwidth = db.Column(db.)
    
    # Either someone is banned or not banned.
    # Problematic users, nazis, etc should be banned without mercy or guilt.
    # Just fucking do it, they aren't worth having around.
    # You shouldn't even have to think about it. Do it. Do it now.
    # Unless a deletion is desired. In which case, there is a way to do this.
    banned = db.Column(db.Boolean())
    # Profile customizations enabled/disabled for this account
    disable_profile_customizations = db.Column(db.Boolean())
    
    
class Identity(db.Model):
    """An account can have more than one identity. Each identity connects an 
    account to a single ActivityPub actor.
    
    Identities hold all of the profile customization details that are not
    contained within an actor model.
    """
    __tablename__ = 'identities'
    
    id = db.Column(db.Integer(), primary_key=True)
    actor_id = db.Column(db.Column(), db.ForeignKey('actors.id'))
    
    # Non-standard profile customizations
    page_background_color = db.Column(db.String())
    page_background_image = db.Column(db.String())
    page_background_tiled = db.Column(db.Boolean())
    page_background_static = db.Column(db.Boolean())
    section_background_color = db.Column(db.String())
    section_header_image = db.Column(db.String())
    section_text_color = db.Column(db.String())
    section_text_shadow = db.Column(db.Boolean())
    section_text_shadow_color = db.Column(db.Boolean())
    # Can be disabled
    disabled = db.Column(db.Boolean())
    # Can be soft deleted. To permanently delete, delete the associated account.
    # This is done to prevent abuse in the form of rapidly created temporary
    # accounts being used to torment and then removed after a block/mute.
    deleted = db.Column(db.Boolean())
    
    
class Blog(db.Model):
    """An account can have more than one blog. Each blog connects an 
    account to a single ActivityPub actor.
    """
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer(), primary_key=True)
    actor_id = db.Column(db.Column(), db.ForeignKey('actors.id'))
    
    # Non-standard profile customizations
    page_background_color = db.Column(db.String())
    page_background_image = db.Column(db.String())
    page_background_tiled = db.Column(db.Boolean())
    page_background_static = db.Column(db.Boolean())
    section_background_color = db.Column(db.String())
    section_header_image = db.Column(db.String())
    section_text_color = db.Column(db.String())
    section_text_shadow = db.Column(db.Boolean())
    section_text_shadow_color = db.Column(db.Boolean())
    # Can be disabled
    disabled = db.Column(db.Boolean())
    # Can be soft deleted. To permanently delete, delete the associated account.
    # This is done to prevent abuse in the form of rapidly created temporary
    # accounts being used to torment and then removed after a block/mute.
    deleted = db.Column(db.Boolean())
    
    
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
    account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'))
    target_actor_id = db.Column(db.Integer(), db.ForeignKey('actors.id'))
    created = db.Column(db.DateTime())
    
    
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
    account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'))
    target_actor_id = db.Column(db.Integer(), db.ForeignKey('actors.id'))
    created = db.Column(db.DateTime())
    
    
class Filter(db.Model):
    """Filters are best described as a more nuanced version of muting, allowing
    specific words to be removed from a timeline or minimized within the 
    timeline.
    """
    __tablename__ = 'filters'
    
    id = db.Column(db.Integer(), primary_key=True)
    account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'))
    
    query = db.Column(db.String)
    hide = db.Column(db.Boolean)
    minimize = db.Column(db.Boolean)
    filter_actor_id = db.Column(db.Integer(), db.ForeignKey('actors.id'))
    
    created = db.Column(db.DateTime())
    duration = db.Column(db.Interval())
    forever = db.Column(db.Boolean())
    
    
class Feed(db.Model):
    """A feed is a set of actors that you want to create a custom timeline
    for. As an example, you could create a feed labeled "friends" for calling
    out your friends' blog posts and statuses.
    
    It's worth noting that you need to subscribe to an actor before this works.
    """
    __tablename__ = 'feeds'
    
    id = db.Column(db.Integer(), primary_key=True)
    identity_id = db.Column(db.Integer(), db.ForeignKey('identities.id'))
    
    
class FeedActor(db.Model):
    """A single actor watched by a feed."""
    __tablename__ = 'feed_actors'
    
    id = db.Column(db.Integer(), primary_key=True)
    feed_id = db.Column(db.Integer(), db.ForeignKey('feeds.id'))
    target_actor_id = db.Column(db.Integer(), db.ForeignKey('actors.id'))
        
    
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
    