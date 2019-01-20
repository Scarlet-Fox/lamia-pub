# License header will go here when I pick one.
from lamia import alchemy as db

class Actor(db.Model):
    # A user is an 'actor' in activitypub lingo
    # Within lamia, users are puppets for identities
    # and blogs locally and all kinds of fun stuff
    # in the broader fediverse.
    id = db.Column(db.Integer, primary_key=True)
    
    # Ap_id is the unique global identifier for this actor
    ap_id = db.Column(db.String)
    ap_type = db.Column(db.String)
    # Keys help you hide things
    public_key = db.Column(db.String)
    
    # Identification stuff
    display_name = db.Column(db.String)
    user_name = db.Column(db.String)
    domain = db.Column(db.String)
    
    # Niceties supported by a lot of instances
    avatar_url = db.Column(db.String)
    header_url = db.Column(db.String)
    
    # Counters for convenience
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)
    
    # ActivityPub streams
    inbox = db.Column(db.String)
    outbox = db.Column(db.String)
    liked = db.Column(db.String)
    following = db.Column(db.String)
    followers = db.Column(db.String)
    
    last_updated = db.Column(db.DateTime, nullable=True)
    
class Account(db.Model):
    # In summary: Accounts are just identity containers
    # and someone can have many identities.
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String)
    private_key = db.Column(db.String)
    
    # Just use bcrypt
    password = db.Column(db.String)
    password_reset_token = db.Column(db.String)
    password_reset_token_date = db.Column(db.String)
    
    join_date = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime, nullable=True)
    
class Identity(db.Model):
    # This is a bit confusing at first, but it shouldn't be
    # in the actual interface. Basically, a local identity
    # is just an ap actor.
    id = db.Column(db.Integer, primary_key=True)
    
    # An identity belongs to a single account
    account_id = db.Column(db.Integer, db.ForeignKey('account.id',
        name="fk_identity_account", ondelete="CASCADE"), index=True)
    # An identity has an associated user, where user is just
    # an acvitivitypub actor type 'Person'
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_identity_actor", ondelete="CASCADE"), index=True)
        
    # This may be a mistake, but basically, you don't want
    # multiple identities sharing the same name.
    # I just saw the trailer for Us (2019). Doppelgangers suck. 
    display_name = db.Column(db.String, unique=True)
    
    # Locked identity - followers are manually approved
    locked = db.Column(db.Boolean, default=False)
    
    # This isn't as confusing as it seems. Most local users will
    # only ever have a single identity. In which case, the
    # complexity remains hidden from them.
    
    # However, multiple accounts may be useful, for things like
    # roleplay characters, lewd/non-lewd, private/public, 
    # plurals, etc.
    
class Filter(db.Model):
    # Filters can be used to minimize ("content warn") content
    id = db.Column(db.Integer, primary_key=True)
    # Simple wildcards can be used, mebbe
    query = db.Column(db.String)
    # Or the content can just not
    hide = db.Column(db.Boolean)
    # Can be temporary
    expiration_date = db.Column(db.DateTime, nullable=True)
    
    # Account-wide filters are active as long as they
    # exist on any identity attached to an account.
    account_wide = db.Column(db.Boolean)
    
    # Filters are set on an identity level
    identity_id = db.Column(db.Integer, db.ForeignKey('identity.id',
        name="fk_filter_identity", ondelete="CASCADE"), index=True)
    
class Follow(db.Model):
    # These are the subscriptions for our local actors
    id = db.Column(db.Integer, primary_key=True)
    # Actors follow things
    follower = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_actor_following", ondelete="CASCADE"), index=True)
    # We can follow actors
    being_followed = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_actor_being_followed", ondelete="CASCADE"), index=True)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
        
class PendingFollow(db.Model):
    # If someone follows you and you have a private/locked account then one
    # of these is created.
    id = db.Column(db.Integer, primary_key=True)
    # Actors can request to follow a local actor
    requested_by = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_follow_requested_by_actor", ondelete="CASCADE"), index=True)
    request_for_actor = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_follow_pending_for_actor", ondelete="CASCADE"), index=True)
    # Approval status, rejecting a follow can optionally be a block btw
    accepted = db.Column(db.Boolean)
    # Insistence on following should prob not be possible
    # blocked follows autoreject when they're made again
    blocked = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
class ActorMute(db.Model):
    # If a mute exists, the muting actor will not see toots 
    # and should also prevent boosts bc um, i muted them
    id = db.Column(db.Integer, primary_key=True)
    muting_actor = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_mute_belongs_to_actor", ondelete="CASCADE"), index=True)
    muted_actor = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_mute_is_muting_actor", ondelete="CASCADE"), index=True)

    created = db.Column(db.DateTime)
    
class ActorBlock(db.Model):
    # A block prevents all interaction - breaks mutual follows,
    # prevents all notifications, removes actors from your sight
    id = db.Column(db.Integer, primary_key=True)
    blocking_actor = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_block_belongs_to_actor", ondelete="CASCADE"), index=True)
    blocked_actor = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_block_is_blocking_actor", ondelete="CASCADE"), index=True)

    created = db.Column(db.DateTime)
    
class Notification(db.Model):
    # Lamia should group up notifications based on object
    # and describe them based on type.
    id = db.Column(db.Integer, primary_key=True)
    # Link back to the original activity for some flexibility
    # in implementing certain things after the fact.
#    activity = FK to ap activity
    ap_object = db.Column(db.String, index=True)
    ap_type = db.Column(db.String, index=True)

    # If a notification is successfully sent to a client
    # of some kind then it was "seen".
    seen = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    
class ActorFeed(db.Model):
    # You can create named feeds that collect actor activity
    id = db.Column(db.Integer, primary_key=True)
    # They have names, names have power
    name = db.Column(db.String)
    # Maybe we can add some context clues here for feeds
    # context = ???
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
class ActorFeedSource(db.Model):
    # Just an actor to keep up with using a feed
    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.Integer, db.ForeignKey('actor.id',
        name="fk_feed_source_actor", ondelete="CASCADE"), index=True)
    feed = db.Column(db.Integer, db.ForeignKey('feed.id',
        name="fk_feed_source_feed", ondelete="CASCADE"), index=True)
    