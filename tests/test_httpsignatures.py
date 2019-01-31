import pytest
import base64
# Import lamia either from pythonpath or a relative parent dir
try:
    import lamia
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())
    
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from lamia.utilities.httpsigs import sign
from lamia.utilities.httpsigs import verify


key = RSA.generate(2048)
private = key.export_key("PEM")
public = key.publickey().export_key("PEM")

headers_no_digest = {'host': 'lamia.social'}
faulty_headers = {'host': 'seems.legit'}
message_body = '{"a key": "a value", "another key": "btw, this is json, obviously"}'
path = '/inbox'
keyId = 'https://lamia.social/lamia#main-key'
body_digest = base64.b64encode(SHA256.new(message_body.encode()).digest())
headers_with_digest = {'host': 'lamia.social', 'digest': f'SHA-256={body_digest}'}
faulty_headers_with_digest = {'host': 'seems.legit', 'digest': f'SHA-256={body_digest}'}


def test_http_signatures_no_digest():
    headers = headers_no_digest.copy()
    signature_header = sign(private, keyId, headers_no_digest, path)
    headers['signature'] = signature_header
    assert verify(public, headers, 'POST', '/inbox', message_body)
    assert verify(public, headers, 'POST', '/lamia/inbox', message_body) == False
    assert verify(public, headers, 'GET', '/inbox', message_body) == False
    
    headers = faulty_headers.copy()
    headers['signature'] = signature_header
    assert verify(public, headers, 'POST', '/inbox', message_body) == False
        
    
def test_http_signatures_digest():
    headers = headers_with_digest.copy()
    signature_header = sign(private, keyId, headers_with_digest, path)
    headers['signature'] = signature_header
    assert verify(public, headers, 'POST', '/inbox', message_body)
    assert verify(public, headers, 'POST', '/lamia/inbox', message_body) == False
    assert verify(public, headers, 'GET', '/inbox', message_body) == False
    
    headers = faulty_headers_with_digest.copy()
    headers['signature'] = signature_header
    assert verify(public, headers, 'POST', '/inbox', message_body) == False