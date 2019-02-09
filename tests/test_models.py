import pytest
# Import lamia either from pythonpath or a relative parent dir
try:
    import lamia
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())

from lamia.models.activitypub import *
from lamia.models.administration import *
from lamia.models.features import *
from lamia.models.moderation import *
from lamia.models.oauth import *
