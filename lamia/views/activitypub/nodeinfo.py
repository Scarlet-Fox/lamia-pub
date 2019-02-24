"""This module contains the views associated with the nodeinfo protocol. While
nodeinfo is not an explicit standard like ActivittyPub or webfinger, it is a
standard practice among fediverse server software.

> https://github.com/jhass/nodeinfo

If a more official standard pops into being later, then it would be
straightforward to implement.

(Note: Our implementation of nodeinfo is pretty basic but gets the job done.)
"""
from starlette.responses import JSONResponse
from starlette.requests import Request
from lamia.utilities import get_request_base_url
from lamia.utilities import get_site_stats
from lamia.version import VERSION, NAME, DESCRIPTION


async def nodeinfo_index(request: Request) -> JSONResponse:
    """Replies to a request with a JSON Resource Descriptor (JRD) document that
    references lamia's implemented nodeinfo schema(s).

    Currently, we only implement nodeinfo's 2.0 schema.
    """

    return JSONResponse({
        'links': [{
            'rel': 'http://nodeinfo.diaspora.software/ns/schema/2.0',
            'href': f'{get_request_base_url(request)}/nodeinfo/2.0.json'
        }]
    })


async def nodeinfo_schema_20(request: Request) -> JSONResponse:  # pylint: disable=unused-argument
    """Provides a basic implementation of nodeinfo's 2.0 schema."""
    site_stats = await get_site_stats()

    return JSONResponse(
        {
            'version': '2.0',
            'software': {
                'name': NAME,
                'description': DESCRIPTION,
                'version': VERSION
            },
            'protocols': [
                'activitypub',
            ],
            'services': {
                'inbound': [],
                'outbound': []
            },
            'openRegistrations': site_stats['open_registration'],
            'usage': {
                'users': {
                    'total': site_stats['local_users']
                },
                'localPosts': site_stats['local_posts']
            }
        },
        headers={
            'content-type':
            'application/json; profile="http://nodeinfo.diaspora.software/ns/schema/2.0#"'
        })
