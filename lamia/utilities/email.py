import asyncio
import sys
import logging
from email.mime.text import MIMEText

import aiosmtplib as smtp
import aiosmtplib.status as status
from starlette.datastructures import URL

import lamia

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
        self.STUBBED = (self.config('DEBUG', cast=bool, default=False)
                       and (not self.config('DEV_EMAIL', cast=bool, default=False)))

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
            self.mail_queue = asyncio.Queue() # No max size, we dont want to drop emails
            self.workers = [asyncio.create_task(self.send_mail_worker()) for _ in range(self.config('MAIL_WORKER_COUNT', default=10))]

        await self.send_html_template_email(
            "Hello World!", "mail_generic.html",
            {"message":"Hello World Too!"},
            self.config('ADMIN_EMAIL')
        )  #TODO: Only here for testing, do not allow into master.

    async def send_mail_catch_error(self, client, message):
        try:
                r = await client.connect()
                if r.code == status.SMTPStatus.ready:
                    if self.dsn.password: # Authenticate if password provided
                        response = await conn.login(self.dsn.username,
                                                    self.dsn.password)
                        if response.code != status.SMTPStatus.auth_successful:
                            logging.error((
                                "Email authorisation failure. Server response: %s\n"
                                "Please check the username and password provided in the config "
                                "and ensure that it is correct."), response)
                    await client.send_message(message)

        except smtp.errors.SMTPRecipientsRefused as e:
                logging.error("EMAIL: Email send attempt failed to users %s", e)

        except smtp.errors.SMTPConnectError as e:
                logging.error("EMAIL: Email connection attempt to SMTP server failed.\n\t%s", e)

        client.close()

    async def send_mail_worker(self):
        client = smtp.SMTP(hostname=self.dsn.hostname, port=self.dsn.port)
        try:
            while True:
                message = await self.mail_queue.get()
                await asyncio.shield(self.send_mail_catch_error(client, message))
                self.mail_queue.task_done()
        except asyncio.CancelledError:
            # Before we allow the cancelation to take effect, clear out emails that still need sending
            while not self.mail_queue.empty():
                message = await self.mail_queue.get()
                await asyncio.shield(self.send_mail_catch_error(client, message))
                self.mail_queue.task_done()
            raise
        finally:
            pass

    async def send_plain_email(self, subject, message, to):
        """
        Sends a plain text email.

        subject: str - subject of the email
        Message: str - Content of the message
        To: list of str - list of email addresses to send to

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

    async def send_html_template_email(self, subject, template, content, to):
        """
        Generates and sends an HTML email from a template.

        subject: str - subject of the email
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

    async def shutdown(self) -> None:
        # we want to make sure that any emails that still need to be sent are either
        # preserved or sent properly.
        if not self.STUBBED: # No need to shut down workers that never got made.
            logging.info("EMAIL: Shutting down email workers")
            for worker in self.workers:
                worker.cancel()
                try:
                    await worker
                except asyncio.CancelledError:
                    logging.debug("EMAIL: Worker cancelled")
                    pass
