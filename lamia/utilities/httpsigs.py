"""This module contains the other, non-webfinger toolkit for federating
through the activitypub protocol - the http signatures.

The official spec for http signing is here: 
https://tools.ietf.org/id/draft-cavage-http-signatures-08.html

The instructions for pycryptodome's glorious RSA stuff is here:
https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html

Some specs on RSA for the curious:
https://tools.ietf.org/html/rfc8017

This was a useful reference because it's mastodon compatible:
https://blog.joinmastodon.org/2018/06/how-to-implement-a-basic-activitypub-server/

The digest header isn't in the above article, but it is in the mastodon source
code, so we will be doing the same thing that mastodon does:
`"SHA-256=#{Digest::SHA256.base64digest(request_body)}"`

There's no date header in the mastodon source code, so I'm not sure that we
need to go that route.
"""

import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

    
def sign(private_key, key_id, headers, path):
    """Returns a raw signature string that can be plugged into a header and
    used to verify the authenticity of an HTTP transmission.
    
    As to the methodology, well... Basically, we're gonna do it this way
    because mastodon does it this way.
    
    It also makes sense, I suppose.
    """
    
    # Take the headers and build a digest for signing
    signed_headers = headers.keys()
    signed_headers.update({
        '(request-target)': f' {path}',
    })
    signed_header_text = ''
    signed_header_keys = signed_headers.keys()
    for header in signed_header_keys:
        signed_header_text.append(f'{header}: {signed_headers[{header}]}')
    signed_header_text = signed_header_text.strip()
    header_digest = SHA256.new(signed_header_text.encode()).digest()
    
    # Sign the digest
    raw_signature = pkcs1_15.new(key).sign(header_digest)
    signature = base64.b64encode(raw_signature)
    
    # Put it into a valid HTTP signature format and return
    signature_dict = {
        'keyId': key_id,
        'algorithm': 'rsa-sha256',
        'headers': ' '.join(signed_header_keys),
        'signature': signature.decode()
    }
    signature_header = ','.join([f'{k}="{v}"' for k, v in signature_dict])
    return signature_header