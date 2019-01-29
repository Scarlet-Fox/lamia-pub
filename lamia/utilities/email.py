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

    We actually do not have a constant connection to the SMTP server
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
        self.STUBBED = self.config('DEBUG', cast=bool, default=False) and (not self.config('DEV_EMAIL', cast=bool, default=False))

        if not self.config('MAIL_DSN', default=False) and not self.STUBBED:
            sys.exit("Configuration failure:\n"
                     "The configuration setting MAIL_DSN was not set, as a result, "
                     "the email subcomponent could not be enabled.\n"
                     "Please set this option before attempting to run again.")

        if self.STUBBED:
            logging.info("Email has been stubbed according to settings in the config file. No emails will be sent.")
        else:
            self.dsn = self.config('MAIL_DSN', cast=URL)

        await self.send_email("Server has started up!")

    async def send_email(self, message) -> bool:
        """
        Returns true if the message sent without issue.
        """
        if self.STUBBED:
            logging.info("Email send attempt was stubbed")
            return True

        async with smtp.SMTP(hostname=self.dsn.hostname, port=self.dsn.port) as conn:
            if self.dsn.password:
                response = conn.login(self.dsn.username, self.dsn.password)
                if response.code != status.SMTPStatus.auth_successful:
                    logging.info(("Email authorisation failure. Server response: {}\n".format(response)+
                             "Please check the username and password provided in the config "+
                             "and ensure that it is correct."))
            message = MIMEText(message)
            message['From'] = self.dsn.username + "@"+self.dsn.hostname
            message['To'] = "test@mail.com"
            message['Subject'] = "hello world!"
            await conn.send_message(message)


    async def shutdown(self) -> None:
        # we want to make sure that any emails that still need to be sent are either
        # preserved or sent properly. 
        pass
