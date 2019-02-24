"""Basic lamia utilities that don't need their own module."""
from starlette.requests import Request
from lamia.translation import _


def get_request_base_url(request: Request) -> str:
    """Returns a base url based on a request."""

    if not request.url.port in ('443', '80'):
        return f'{request.url.scheme}://{request.url.hostname}:{request.url.port}'

    return f'{request.url.scheme}://{request.url.hostname}'


async def get_site_stats() -> dict:
    """Returns a dict of commonly requested site statistics and information.
    While this function primarily exists for compiling nodeinfo responses, it
    is also available for other views that may display statistical information.

    TODO: The data for this should be stored in a redis cache.
    TODO: Everything here is currently filler. We obs need real queries.
    """

    local_users = 0
    local_posts = 0
    open_registration = True

    return {
        'local_users': local_users,
        'local_posts': local_posts,
        'open_registration': open_registration
    }


def response_contains_graphql_error(response: dict,
                                    error_message: str) -> bool:
    """Given a graphql result and an error message, checks through the result
    to see if the error message is included in response['errors'].
    """

    if response is None:
        raise Exception(_('Response is null.'))

    if 'errors' not in response:
        return False

    if response['errors'] == []:
        return False

    found_error = False
    for error in response['errors']:
        if error['message'] == _(error_message):
            found_error = True

    return found_error
