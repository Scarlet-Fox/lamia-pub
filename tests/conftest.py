import sys
import os
sys.path.append(os.getcwd())
import asyncio

import pytest

from lamia.models.activitypub import *
from lamia.models.administration import *
from lamia.models.features import *
from lamia.models.moderation import *
from lamia.models.oauth import *

from lamia.database import db
from lamia.config import DEV_CONFIG

if not DEV_CONFIG:
    raise Exception('Please create a lamia.dev.config file before running tests.')

@pytest.fixture(scope='module')
def sa_engine():
    asyncio.get_event_loop().run_until_complete(db.gino.create_all())
    yield db
    asyncio.get_event_loop().run_until_complete(db.gino.drop_all())
