"""Models that pertain directly to the messy business of keeping an online
environment safe from harmful intentions are in this module.

Moderators should ban nazis, by the way. This shouldn't need to be said, but
it is being said right here. Get rid of them.
"""
from gino.dialects.asyncpg import JSONB

from .. import db


class ModerationLog(db.Model):
    """Quis custodiet ipsos custodes?

    Instance admins and other moderators should keep an eye on log entries
    and log entries should result in notifications, in theory.
    """
    __tablename__ = 'moderation_logs'
    description = db.Column(db.String())

    created = db.Column(db.DateTime())
    created_by_account_id = db.Column(db.Integer(),
                                      db.ForeignKey('accounts.id'))


class Import(db.Model):
    """Followed, muted, and blocked actors can be imported from ActivityPub
    files.

    These imports should not run automatically because of the potential
    for abuse, particularly from "follow" actions. Instead, they are stored here
    and can be selectively authorized to move forward by moderators.
    """
    __tablename__ = 'imports'

    id = db.Column(db.Integer(), primary_key=True)

    request_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='CASCADE'),
    )
    request_for_identity_id = db.Column(
        db.Integer(),
        db.ForeignKey('identities.id', ondelete='CASCADE'),
    )
    data_to_import = db.Column(JSONB())

    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())
    processed = db.Column(db.DateTime())

    allowed = db.Column(db.Boolean())


REPORT_STATUSES = {
    'ignored': 'will not address',
    'open': 'received, no action done yet',
    'feedback': 'paused, waiting for feedback',
    'waiting': 'waiting for action',
    'actiontaken': 'action has been taken',
    'working': 'someone is already looking into this',
    'escalation': 'an admin is requested to look into this',
}


class Report(db.Model):
    """Reports are a necessary part of any online social environment. They are
    a way to flag local content for moderators on a local site, and they
    can be created and sent to this site from other sites.
    """
    __tablename__ = 'reports'

    id = db.Column(db.Integer(), primary_key=True)
    original_content = db.Column(db.String())
    content_uri = db.Column(db.String())
    target_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='SET NULL'),
        nullable=True,
    )

    report_by_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='SET NULL'),
        nullable=True,
    )
    current_status = db.Column(db.String())
    assigned_to_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True,
    )
    comment_count = db.Column(db.Integer())

    created = db.Column(db.DateTime())
    last_updated = db.Column(db.DateTime())
    resolved = db.Column(db.Boolean())
    marked_resolved_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class ReportComment(db.Model):
    """Allow moderator to moderator talk in a report, should work like chat
    messages."""
    __tablename__ = 'report_comments'

    message = db.Column(db.String())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)
    created = db.Column(db.DateTime())

    report_id = db.Column(db.Integer(), db.ForeignKey('reports.id'))
    # Changing the status of a report should create a comment where the message
    # is something like 'changed status from ignored to open'.
    status_change = db.Column(db.Boolean())


class ActorCensor(db.Model):
    """An actor censor is a light server to client moderation action.

    An actor censor is a created at the server level, and forces an actors'
    activities to either appear content warned or minimized.
    """
    __tablename__ = 'actor_censors'

    id = db.Column(db.Integer(), primary_key=True)
    target_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='CASCADE'),
    )
    created = db.Column(db.DateTime())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class ActorMute(db.Model):
    """An actor block is a moderate server to client moderation action.

    An actor mute is a created at the server level, and either hides the actor's
    activities from the federated timeline or minimizes them.
    """
    __tablename__ = 'actor_mutes'

    id = db.Column(db.Integer(), primary_key=True)
    target_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='CASCADE'),
    )
    created = db.Column(db.DateTime())
    duration = db.Column(db.Interval())
    forever = db.Column(db.Boolean())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class ActorBlock(db.Model):
    """An actor block is a severe server to client moderation action.

    An actor block is a created at the server level, and probits the blocked
    actor from interacting with the site. It also breaks follows between
    actors on this site and the actor that is blocked.
    """
    __tablename__ = 'actor_blocks'

    id = db.Column(db.Integer(), primary_key=True)
    target_actor_id = db.Column(
        db.Integer(),
        db.ForeignKey('actors.id', ondelete='CASCADE'),
    )
    created = db.Column(db.DateTime())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class DomainCensor(db.Model):
    """A domain censor is a light server to server moderation action.

    An domain censor is a created at the server level, and forces all activities
    from a specific domain to either appear content warned or minimized.
    """
    __tablename__ = 'domain_censors'

    id = db.Column(db.Integer(), primary_key=True)
    domain = db.Column(db.String())
    created = db.Column(db.DateTime())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class DomainMute(db.Model):
    """A domain mute is a moderate server to server moderation action.

    A domain mute is a created at the server level, and either hides the domains'
    activities from the federated timeline or minimizes them.
    """
    __tablename__ = 'domain_mutes'

    id = db.Column(db.Integer(), primary_key=True)
    domain = db.Column(db.String())
    created = db.Column(db.DateTime())
    duration = db.Column(db.Interval())
    forever = db.Column(db.Boolean())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class DomainBlock(db.Model):
    """A domain block is a severe server to client moderation action.

    A domain block is a created at the server level, and probits all actors on
    a blocked site from interacting with the local site. It also breaks
    follows between actors on this site and the site that is blocked.
    """
    __tablename__ = 'domain_blocks'

    id = db.Column(db.Integer(), primary_key=True)
    domain = db.Column(db.String())
    created = db.Column(db.DateTime())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)


class DomainEmailBlock(db.Model):
    """Email domain blocks prevent harmful registrations and registrations
    from spammers.
    """
    __tablename__ = 'domain_email_block'

    id = db.Column(db.Integer(), primary_key=True)
    domain = db.Column(db.String())
    created = db.Column(db.DateTime())
    created_by_account_id = db.Column(
        db.Integer(),
        db.ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True)
