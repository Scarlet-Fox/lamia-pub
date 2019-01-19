# License header will go here when I pick one.
from lamia import alchemy as db

class User(db.Model):
    # A user is an 'actor' in activitypub lingo
    id = db.Column(db.Integer, primary_key=True)
    
    # Ap_id is the unique global identifier for this actor
    ap_id = db.Column(db.String)
    ap_type = db.Column(db.String)
    # Keys help you hide things
    public_key = db.Column(db.String)
    
    # Identification stuffz
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
        name="fk_identity_user", ondelete="CASCADE"), index=True)
    
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
    
