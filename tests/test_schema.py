import pytest
# Import lamia either from pythonpath or a relative parent dir
try:
    import lamia
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())

from lamia.activitypub.schema import PubActivity, PubObject, PubActor


well_formed_activity = {
	'id': 'https://lamia.social/l/activities/101016339929195685',
	'type': 'Announce',
	'actor': 'https://lamia.social/scarly',
	'published': '2018-11-05T03:03:42Z',
	'to': [
		'https://www.w3.org/ns/activitystreams#Public'
	],
	'cc': [
		'https://lamia.social/u/chel',
		'https://lamia.social/u/scarly/followers'
	],
	'object': 'https://lamia.social/l/statuses/101014122824442242',
}


badly_formed_activity = {}

def test_activity_schema():
    activity = PubActivity(well_formed_activity)
    assert activity.validate() == True

    activity.load_json_ld(badly_formed_activity)
    assert activity.validate() == False
    
    assert '@context' in activity.to_json_ld()


well_formed_object = {
	'id': 'https://lamia.social/l/statuses/101014122824442242',
	'type': 'Note',
	'summary': 'this is an example cw',
	'inReplyTo': 'https://lamia.social/l/statuses/101014122824442243',
	'published': '2018-11-05T02:31:49Z',
	'url': 'https://lamia.social/l/statuses/101014122824442242',
	'attributedTo': 'https://lamia.social/u/scarly',
	'to': [
		'https://www.w3.org/ns/activitystreams#Public'
	],
	'cc': [
		'https://lamia.social/u/scarly/followers'
	],
    
	'sensitive': True,
	'content': '<p>This is a test.</p>',
	'contentMap': {
		'en': '<p>This is a test.</p>'
	},
	'attachment': [

	],
	'tag': [

	],
}


badly_formed_object = {}


def test_object_schema():
    _object = PubObject(well_formed_object)
    assert _object.validate() == True
    
    _object.load_json_ld(badly_formed_object)
    assert _object.validate() == False

    assert '@context' in _object.to_json_ld()

well_formed_actor = {
	"id": "https://lamia.social/u/scarly",
	"type": "Person",
	"following": "https://lamia.social/u/scarly/following",
	"followers": "https://lamia.social/u/scarly/followers",
	"inbox": "https://lamia.social/u/scarly/inbox",
	"outbox": "https://lamia.social/u/scarly/outbox",
	"featured": "https://lamia.social/u/scarly/collections/featured",
	"preferredUsername": "scarly",
	"name": "Scarly Crow",
	"summary": "<p>a description of an actor</p>",
	"url": "https://lamia.social/u/scarly",
	"manuallyApprovesFollowers": False,
	"publicKey": {
		"id": "https://lamia.social/u/scarly#main-key",
		"owner": "https://lamia.social/u/scarly",
		"publicKeyPem": "-----BEGIN PUBLIC KEY-----this is actually nonsense-----END PUBLIC KEY-----\n"
	},
	"tag": [

	],
	"attachment": [
		{
			"type": "PropertyValue",
			"name": "Species",
			"value": "crow (sometimes a werecat)"
		},
	],
	"endpoints": {
		"sharedInbox": "https://lamia.social/inbox"
	},
	"icon": {
		"type": "Image",
		"mediaType": "image/png",
		"url": "media/scarly_avatar.png"
	},
	"image": {
		"type": "Image",
		"mediaType": "image/png",
		"url": "media/scarly_header.png"
	},
}

badly_formed_actor = {}


def test_actor_schema():
    actor = PubActor(well_formed_actor)
    assert actor.validate() == True
    
    actor.load_json_ld(badly_formed_actor)
    assert actor.validate() == False
    
    assert '@context' in actor.to_json_ld()
