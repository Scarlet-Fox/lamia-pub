import sys
import os
sys.path.append(os.getcwd())

import tempfile
import asyncio
import mailbox
import aiosmtpd.controller
import aiosmtpd.handlers
import starlette.config
import pytest
import lamia.utilities.email

TEST_PORT = 12345

@pytest.fixture
@pytest.mark.asyncio
async def email_client():
    config = starlette.config.Config(environ={"DEBUG":"True", "MAIL_DSN":"smtp://test@localhost:{}".format(TEST_PORT), "DEV_EMAIL":"True"})
    email = lamia.utilities.email.Email(config=config)
    await email._startup() # Dont need the app to run these tests.
    yield email
    await email._shutdown()


# This is just the path to directory that will have emails when they are sent.
@pytest.fixture
@pytest.mark.asyncio
async def email_server_outdir(): # Only used for testing.
    # make a folder to store caught emails in 
    with tempfile.TemporaryDirectory() as tempdir:
        maildir = os.path.join(tempdir, 'maildir')
        controller = aiosmtpd.controller.Controller(aiosmtpd.handlers.Mailbox(maildir), port=TEST_PORT)
        controller.start()
        yield maildir

@pytest.mark.asyncio
async def test_email(email_client, email_server_outdir):
    # We dont test the send email methods because they are just arg wrappers
    await email_client.send_plain_email("test_email","test_email","you@me.com")
    await asyncio.sleep(1)
    mail = mailbox.Maildir(email_server_outdir)
    # Get what should be only email, throw out key value, check subject.
    assert mail.popitem()[1]['Subject'] == "test_email"

