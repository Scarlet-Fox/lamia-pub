from .. import db


class OauthToken(db.Model):
    """A token created for our lovely API."""
    __tablename__ = 'oauth_tokens'
    
    id = db.Column(db.Integer(), primary_key=True)
    app_id = db.Column(
        db.Integer(), 
        db.ForeignKey('oauth_applications.id', ondelete='CASCADE')
    )
    account_id = db.Column(
        db.Integer(), 
        db.ForeignKey('accounts.id', ondelete='CASCADE')
    )
    
    access_token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    expires = db.Column(db.DateTime())
    created = db.Column(db.DateTime())

class OauthApplication(db.Model):
    """An external application or service."""
    __tablename__ = 'oauth_applications'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    website = db.Column(db.String())
    
    redirect_uri = db.Column(db.String())
    scopes = db.Column(db.String())
    client_id = db.Column(db.String())
    client_secret = db.Column(db.String())
    
    owner_id = db.Column(db.Integer())
    
    created = db.Column(db.DateTime())
    last_updated = db.Column(db.String())