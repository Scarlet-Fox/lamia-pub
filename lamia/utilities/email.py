"""Lamia wrapper around aiosmtplib"""
import asyncio
import sys
import logging
import typing
from email.mime.text import MIMEText

import aiosmtplib as smtp
import aiosmtplib.status as status
import starlette
from starlette.datastructures import URL

import lamia




class Email():
    """
    Lamia wrapper around aiosmtplib

    Pluggable into any starlette app.

    app: the starlette app to register to Email
    config: The starlette configuration object

    raises: Value error if app or config are provided but not both
    """

    def init_app(self, app: starlette.applications.Starlette,
                 config: starlette.config.Config) -> None:
        """
        Register the starlette app with the email manager.

        App: the starlette app
        config: lamia's config

        Returns: none
        """
        self.config = config
        app.add_event_handler('startup', self._startup)
        app.add_event_handler('shutdown', self._shutdown)

    def __init__(self,
                 app: starlette.applications.Starlette = None,
                 config: starlette.config.Config = None):
        if (app is not None) != (
                config is not None):  # We were provided one but not both
            raise ValueError(
                "A starlette app or configuration was provided, but not both.")
        if app is not None:
            self.init_app(app, config)

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
                "Email has been stubbed according to settings in the config file. "
                "No emails can be sent.")
        else:
            self.dsn = self.config('MAIL_DSN', cast=URL)
            self.mail_queue = asyncio.Queue(
            )  # No max size, we dont want to drop emails
            self.workers = [
                asyncio.create_task(self._send_mail_worker())
                for _ in range(self.config('MAIL_WORKER_COUNT', default=10))
            ]

        await self.send_html_template_email(
            "Hello World!", "mail_generic.html",
            {"message": "Hello World Too!"}, self.config('ADMIN_EMAIL')
        )  #TODO: Only here for testing, do not allow into master.

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
                        logging.error((
                            "Email authorisation failure. Server response: %s\n"
                            "Please check the username and password provided in the config "
                            "and ensure that it is correct."), response)
                await client.send_message(message)

        except smtp.errors.SMTPRecipientsRefused as e:
            logging.error(
                "EMAIL: Email send attempt failed to users for reason: %s", e)

        except smtp.errors.SMTPConnectError as e:
            logging.error(
                "EMAIL: Email connection attempt to SMTP server failed for reason: %s",
                e)
        except ValueError as e:
            logging.error(
                "EMAIL: Email connection or send attempt failed for reason: %s"
            )

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
            logging.debug("Email send attempt was stubbed")
            return

        message = MIMEText(message)
        message['From'] = self.dsn.username + "@" + self.dsn.hostname
        message['To'] = to
        message['Subject'] = subject

        await self.mail_queue.put(message)

    async def send_html_template_email(self, subject: str, template: str,
                                       content: typing.Dict[str, typing.Any], to):
        """
        Generates and sends an HTML email from a template.

        subject: subject line of the email
        template: valid jinja template
        content: the dictionary to pass on to the jinja template handler.

        As emails are sent using a pool, there is no way to confirm that the email sent.
        This returns nothing.
        """
        if self.STUBBED:
            logging.debug("Email send attempt was stubbed")
            return

        template = lamia.jinja.get_template(template)
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
            logging.info("EMAIL: Shutting down email workers")
            for worker in self.workers:
                worker.cancel()
                try:
                    await worker
                except asyncio.CancelledError:
                    logging.debug("EMAIL: Worker cancelled")
