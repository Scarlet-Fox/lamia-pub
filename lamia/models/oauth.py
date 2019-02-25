"""Oauth2 implementation for lamias everywhere."""
import os
import jwt
import pendulum
from lamia.database import db


class OauthToken(db.Model):
    """A token created for our lovely API."""
    __tablename__ = 'oauth_tokens'

    id = db.Column(db.Integer(), primary_key=True)
    app_id = db.Column(
        db.Integer(), db.ForeignKey(
            'oauth_applications.id', ondelete='CASCADE'))
    account_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'accounts.id', ondelete='CASCADE', name='fk_oauthtoken_account'))

    access_token = db.Column(db.String())
    token_secret = db.Column(db.String())
    expires = db.Column(db.DateTime())
    created = db.Column(db.DateTime())

    def set_access_token(self, payload: dict, days: int = 7) -> str:
        """Encode a payload for this token."""
        now = pendulum.now()
        duration = pendulum.duration(days=days)
        expires = now + duration

        payload['created'] = now.to_iso8601_string()
        payload['expiration'] = expires.to_iso8601_string()

        self.expires = expires.naive()
        self.created = now.naive()

        secret = os.urandom(24).hex()
        self.token_secret = secret
        self.access_token = jwt.encode(
            payload, secret, algorithm='HS256').decode()
        return self.access_token

    def decode_access_token(self, token: str) -> dict:
        """Decode a previously encoded token."""
        return jwt.decode(token, self.token_secret, algorithms=['HS256'])


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
