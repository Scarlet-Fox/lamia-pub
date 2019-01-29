import asyncio
import sys
import logging
from email.mime.text import MIMEText

import aiosmtplib as smtp
import aiosmtplib.status as status
from starlette.datastructures import URL


class Email(object):
    """
    Lamia wrapper around aiosmtplib.SMTP

    We actually do not have a constant connection to the SMTP server.
    These will be constructed and tore down on a per-use basis,
    as aiosmtplib does not have support for concurrent messages on
    one connection.
    """

    def init_app(self, app, config):
        self.config = config
        app.add_event_handler('startup', self.startup)
        app.add_event_handler('shutdown', self.shutdown)

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    async def startup(self):
        # pylint: disable=attribute-defined-outside-init
        # disable this warning, as startup is basically a second init function

        # Using a url might not be the *best* way to do this but it cant be the worst
        # Server must be properly setup if STUBBED is false
        self.STUBBED = self.config(
            'DEBUG', cast=bool, default=False) and (not self.config(
                'DEV_EMAIL', cast=bool, default=False))

        if not self.config('MAIL_DSN', default=False) and not self.STUBBED:
            sys.exit(
                "Configuration failure:\n"
                "The configuration setting MAIL_DSN was not set, as a result, "
                "the email subcomponent could not be enabled.\n"
                "Please set this option before attempting to run again.")

        if self.STUBBED:
            logging.info(
                "Email has been stubbed according to settings in the config file. No emails can be sent."
            )
        else:
            self.dsn = self.config('MAIL_DSN', cast=URL)

        await self.send_plain_email(
            "Hello World!", "Server has started up!",
            self.config('ADMIN_EMAIL')
        )  #TODO: Only here for testing, do not allow into master.

    async def send_plain_email(self, subject, message, to) -> bool:
        """
        Sends a plain text email.
        Returns true if the message sent without issue.
        subject: str - subject of the email
        Message: str - Content of the message
        To: list of str - list of email addresses to send to
        """
        if self.STUBBED:
            logging.info("Email send attempt was stubbed")
            return True

        async with smtp.SMTP(
                hostname=self.dsn.hostname, port=self.dsn.port) as conn:
            if self.dsn.password:
                response = await conn.login(self.dsn.username,
                                            self.dsn.password)
                if response.code != status.SMTPStatus.auth_successful:
                    logging.info((
                        "Email authorisation failure. Server response: {}\n".
                        format(response) +
                        "Please check the username and password provided in the config "
                        + "and ensure that it is correct."))

            message = MIMEText(message)
            message['From'] = self.dsn.username + "@" + self.dsn.hostname
            message['To'] = to
            message['Subject'] = subject
            try:
                await conn.send_message(message)
            except (ValueError, SMTPRecepientsRefused,
                    SMTPResponseException) as e:
                pass

    async def shutdown(self) -> None:
        # we want to make sure that any emails that still need to be sent are either
        # preserved or sent properly.
        pass