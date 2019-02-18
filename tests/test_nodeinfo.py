import sys
import os
sys.path.append(os.getcwd())

import pytest

import ujson as json
from starlette.testclient import TestClient
from lamia import app
from lamia.version import __version__

def test_nodeinfo_index():
    client = TestClient(app)
    
    response = client.get('/.well-known/nodeinfo')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    
    print(response_body)
    nodeinfo_20_listed = False
    for entry in response_body['links']:
        if entry['rel'] == 'http://nodeinfo.diaspora.software/ns/schema/2.0':
            if entry['href'].endswith('/nodeinfo/2.0.json'):
                nodeinfo_20_listed = True
            
    assert nodeinfo_20_listed == True
    
def test_nodeinfo_schema_20():
    client = TestClient(app)
    
    response = client.get('/nodeinfo/2.0.json')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    print(response_body)
    
    assert response_body['version'] == '2.0'
    assert response_body['software']['name'] == 'lamia'
    assert response_body['software']['version'] == __version__
    assert 'activitypub' in response_body['protocols']
    assert isinstance(response_body['services']['inbound'], list)
    assert isinstance(response_body['services']['outbound'], list)
    assert isinstance(response_body['openRegistrations'], bool)
    assert isinstance(response_body['usage']['users']['total'], int)
    assert isinstance(response_body['usage']['localPosts'], int)
    assert response.headers['content-type'] == 'application/json; profile="http://nodeinfo.diaspora.software/ns/schema/2.0#"'
