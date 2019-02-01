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

    private_key - the private key from an rsa key pair
    key_id - the lookup for the key to validate
    headers - should be a dictionary of request headers
    path - the relative url that we're requesting
    """
    # We should probably avoid accidentally changing our headers
    headers = headers.copy()
    # Import the key
    private_key = RSA.import_key(private_key)
    # Note: we assume that this outgoing request is a POST
    headers.update({
        '(request-target)': f'post {path}',
    })
    # Take the headers and build a digest for signing
    signed_header_keys = headers.keys()
    signed_header_text = ''
    for header_key in signed_header_keys:
        signed_header_text += f'{header_key}: {headers[header_key]}\n'
    signed_header_text = signed_header_text.strip()
    header_digest = SHA256.new(signed_header_text.encode('ascii'))

    # Sign the digest
    raw_signature = pkcs1_15.new(private_key).sign(header_digest)
    signature = base64.b64encode(raw_signature).decode('ascii')

    # Put it into a valid HTTP signature format and return
    signature_dict = {
        'keyId': key_id,
        'algorithm': 'rsa-sha256',
        'headers': ' '.join(signed_header_keys),
        'signature': signature
    }
    signature_header = ','.join(
        [f'{k}="{v}"' for k, v in signature_dict.items()])
    return signature_header


def verify(public_key, headers, method, path, body):
    """Returns true or false depending on if the key that we plugged in here
    validates against the headers, method, and path.

    publiuc_key - the public key from an rsa key pair
    headers - should be a dictionary of request headers
    method - the method that was used to make the request
    path - the relative url that was requested from this instance
    body - the received request body (used for digest)

    I'm kind of starting to enjoy this. It's a pity the crypto portion
    of this should be coming to an end soon. Actually, no, no it isn't.
    """
    # Import the key
    public_key = RSA.import_key(public_key)
    # Build a dictionary of the signature values
    signature_header = headers['signature']
    signature_dict = {
        k: v[1:-1]
        for k, v in [i.split('=', 1) for i in signature_header.split(',')]
    }

    # Unpack the signed headers and set values based on current headers and
    # body (if a digest was included)
    signed_header_list = []
    for signed_header in signature_dict['headers'].split(' '):
        if signed_header == '(request-target)':
            signed_header_list.append(
                f'(request-target): {method.lower()} {path}')
        elif signed_header == 'digest':
            body_digest = base64.b64encode(SHA256.new(body.encode()).digest())
            signed_header_list.append(f'digest: SHA-256={body_digest}')
        else:
            signed_header_list.append(
                f'{signed_header}: {headers[signed_header]}')

    # Now we have our header data digest
    signed_header_text = '\n'.join(signed_header_list)
    header_digest = SHA256.new(signed_header_text.encode('ascii'))

    # Get the signature, verify with public key, return result
    signature = base64.b64decode(signature_dict['signature'])

    try:
        pkcs1_15.new(public_key).verify(header_digest, signature)
        return True
    except (ValueError, TypeError):
        return False

    # TODO: Uh, what other algorithms are used in the wild? Mastodon
    # uses rsa-sha256 but it isn't the only thing out there.
    # I guess we'll find out soon.
