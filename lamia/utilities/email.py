"""Lamia wrapper around aiosmtplib and jinja.

Allows sending plain-text and jinja templatted emails.

Adds the following configuration settings:

DEV_EMAIL: A development setting.
    Emails are not send in debug mode unless this is enabled.

MAIL_DSN: A fully qualified URL of the following shape:
    smtp://username[:password]@hostname:port
    username must be a valid account to send emails from on the hostname smtp server.

ADMIN_EMAIL: Email address to send administrative emails to.

MAIL_WORKER_COUNT: Integer number of mail worker's to have running at once.
    This should normally not need changing. Defaults to 10.

MAIL_JINJA_DIR: A directory to find template overrides, so that default templates do
not have to be used.
    If not specified, only default templates stored at the module root will be used.

"""
import asyncio
import sys
import typing
from email.mime.text import MIMEText

import aiosmtplib as smtp
import aiosmtplib.status as status
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import URL
import jinja2

from lamia.logging import logging
from lamia.translation import _


class Email():
    """
    Lamia wrapper around aiosmtplib

    Pluggable into any starlette app.

    app: the starlette app to register to Email
    config: The starlette configuration object

    raises: Value error if only app is provided an argument.
    """

    def init_app(self, app: Starlette, config: Config) -> None:
        """
        Register the starlette app with the email manager.

        App: the starlette app
        config: lamia's config

        Returns: none
        """
        self.config = config
        app.add_event_handler('startup', self._startup)
        app.add_event_handler('shutdown', self._shutdown)

    def __init__(self, app: Starlette = None, config: Config = None):
        self.stubs = []  #
        if (app is not None) and (
                config is
                None):  # We were provided an app with no configuration
            raise ValueError(
                "A starlette app was provided, but no configuration.")
        if app is not None:
            self.init_app(app, config)
        elif config is not None:
            self.config = config

        self.stubs = []  # a list of stubbed emails, if needed.

    async def _startup(self) -> None:
        """
        Startup function intended to be ran on application start.

        Returns: none
        """

        # pylint: disable=attribute-defined-outside-init
        # disable this warning, as startup is basically a second init function

        # Using a url might not be the *best* way to do this but it cant be the worst
        # Server must be properly setup if STUBBED is false
        self.STUBBED = (  # pylint: disable=invalid-name
            self.config('DEBUG', cast=bool, default=False)
            and (not self.config('DEV_EMAIL', cast=bool, default=False)))

        if not self.config('MAIL_DSN', default=False) and not self.STUBBED:
            sys.exit(
                "Configuration failure:\n"
                "The configuration setting MAIL_DSN was not set, as a result, "
                "the email subcomponent could not be enabled.\n"
                "Please set this option before attempting to run again.")

        if self.STUBBED:
            logging.info(
                _("Email has been stubbed according to settings in the config file. "
                  "No emails can be sent."))
        else:
            self.dsn = self.config('MAIL_DSN', cast=URL)
            self.mail_queue = asyncio.Queue(
            )  # No max size, we dont want to drop emails
            self.workers = [
                asyncio.create_task(self._send_mail_worker())
                for _ in range(self.config('MAIL_WORKER_COUNT', default=10))
            ]

        jinja_template = []
        if self.config('MAIL_JINJA_DIR', default=False):
            jinja_template = self.config('MAIL_JINJA_DIR', cast=str)
        self.jinja = jinja2.Environment(
            loader=jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(jinja_template),
                jinja2.PackageLoader('email', 'templates')
            ]))

    async def _send_mail_catch_error(self, client, message):
        """
        Sends a message to an smtp server, catching and handling all exceptions.

        Client: An aiosmtplib.SMTP object, prepared to be connected.
        Message: An email.mime.text.MIMEText object.
        """
        try:
            response = await client.connect()
            if response.code == status.SMTPStatus.ready:
                if self.dsn.password:  # Authenticate if password provided
                    response = await client.login(self.dsn.username,
                                                  self.dsn.password)
                    if response.code != status.SMTPStatus.auth_successful:
                        logging.error(
                            _("Email authorisation failure. Server response: %s\n"
                              "Please check the username and password provided in the config "
                              "and ensure that it is correct."), response)
                await client.send_message(message)

        except smtp.errors.SMTPRecipientsRefused as e:
            logging.error(
                _("EMAIL: Email send attempt failed to users for reason: %s"),
                e)

        except smtp.errors.SMTPConnectError as e:
            logging.error(
                _("EMAIL: Email connection attempt to SMTP server failed for reason: %s"
                  ), e)
        except ValueError as e:
            logging.error(
                _("EMAIL: Email connection or send attempt failed for reason: %s"
                  ))

        client.close()

    async def _send_mail_worker(self):
        """
        Async worker thread to be used internally.

        When started, will clear the mail queue as it becomes avalible to it.

        When cancelled with asyncio.cancel it will clean any remaining emails
        before closing itself out gracefully.
        """
        client = smtp.SMTP(hostname=self.dsn.hostname, port=self.dsn.port)
        try:
            while True:
                message = await self.mail_queue.get()
                await asyncio.shield(
                    self._send_mail_catch_error(client, message))
                self.mail_queue.task_done()
        except asyncio.CancelledError:
            # Before we allow the cancelation to take effect
            # clear out emails that still need sending
            while not self.mail_queue.empty():
                message = await self.mail_queue.get()
                await asyncio.shield(
                    self._send_mail_catch_error(client, message))
                self.mail_queue.task_done()
            raise
        finally:
            pass

    async def send_plain_email(self, subject: str, message: str,
                               to: typing.List[str]):
        """
        Sends a plain text email.

        subject: subject of the email
        Message: Content of the message
        To: list of email addresses to send to

        As emails are sent using a pool, there is no way to confirm that the email sent.
        This returns nothing.
        """
        if self.STUBBED:
            self.stubs.append({
                "Type": "plain",
                "Subject": subject,
                "Message": message,
                "To": to
            })
            logging.debug(_("Email send attempt was stubbed"))
            return

        message = MIMEText(message)
        message['From'] = self.dsn.username + "@" + self.dsn.hostname
        message['To'] = to
        message['Subject'] = subject

        await self.mail_queue.put(message)

    async def send_html_template_email(self, subject: str, template: str,
                                       content: typing.Dict[str, typing.Any],
                                       to):
        """
        Generates and sends an HTML email from a template.

        subject: subject line of the email
        template: valid jinja template
        content: the dictionary to pass on to the jinja template handler.

        As emails are sent using a pool, there is no way to confirm that the email sent.
        This returns nothing.
        """
        if self.STUBBED:
            self.stubs.append({
                "Type": "html",
                "Subject": subject,
                "Template": template,
                "Content": content,
                "To": to
            })
            logging.debug(_("Email send attempt was stubbed"))
            return

        template = self.jinja.get_template(template)
        message = MIMEText(template.render(content), "html")
        message['To'] = to
        message['Subject'] = subject

        await self.mail_queue.put(message)

    async def _shutdown(self) -> None:
        """
        Internal method to clean up on starlette server close.
        """
        # we want to make sure that any emails that still need to be sent are either
        # preserved or sent properly.
        if not self.STUBBED:  # No need to shut down workers that never got made.
            logging.info(_("EMAIL: Shutting down email workers"))
            for worker in self.workers:
                worker.cancel()
                try:
                    await worker
                except asyncio.CancelledError:
                    logging.debug(_("EMAIL: Worker cancelled"))
