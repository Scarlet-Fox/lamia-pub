import pytest
# Import lamia either from pythonpath or a relative parent dir
try:
    import lamia
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())

from lamia.activitypub.schema import Activity


well_formed_activity = {
			"id": "https://lamia.social/l/activities/101016339929195685",
			"type": "Announce",
			"actor": "https://lamia.social/scarly",
			"published": "2018-11-05T03:03:42Z",
			"to": [
				"https://www.w3.org/ns/activitystreams#Public"
			],
			"cc": [
				"https://lamia.social/u/chel",
				"https://lamia.social/u/scarly/followers"
			],
			"object": "https://lamia.social/l/statuses/101014122824442242",
		}


badly_formed_activity = {
			"id": "https://lamia.social/l/activities/101016339929195685",
			"actor": "https://lamia.social/scarly",
			"to": [
				"https://www.w3.org/ns/activitystreams#Public"
			],
			"cc": [
				"https://lamia.social/u/chel",
				"https://lamia.social/u/scarly/followers"
			],
			"object": "https://lamia.social/l/statuses/101014122824442242",
		}


def test_activity_schema():
    activity = Activity(well_formed_activity)
    assert activity.validate() == True

    activity = Activity(badly_formed_activity)
    assert activity.validate() == False