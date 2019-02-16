"""Setup lamia email lifecycle and global."""
# pylint: disable=invalid-name
import lamia.utilities.email as email
import lamia.config as CONFIG

mail = email.Email()


def setup_email(app) -> None:
    """Sets up lifecycle functions."""
    mail.init_app(app, CONFIG.config)
