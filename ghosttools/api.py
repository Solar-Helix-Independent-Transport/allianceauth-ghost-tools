import logging

from corptools.providers import esi_openapi
from ninja import NinjaAPI
from ninja.security import django_auth

logger = logging.getLogger(__name__)

api = NinjaAPI(
    title='Ghost Tools API',
    version='0.0.1',
    urls_namespace='ghosttools:api',
    auth=django_auth,
)


@api.post('ghost/kick', tags=['Ghosts'])
def post_ghost_kick(request, character_id: int):
    """Open a character info window in the linked ghost character's game client."""
    if not request.user.has_perm('ghosttools.access_ghost_tools'):
        return 403, 'Permission Denied'

    try:
        linked = request.user.ghost_character
        online = esi_openapi.client.Location.GetCharactersCharacterIdOnline(
            character_id=linked.token.character_id,
            token=linked.token,
        ).result(use_etag=False)
        if online.online:
            esi_openapi.client.User_Interface.PostUiOpenwindowInformation(
                target_id=character_id,
                token=linked.token,
            ).result()
        return 200, 'Sent Open Request'
    except Exception as e:
        logger.error('Ghost kick error: %s', e)
        return 200, 'Failed to Send Open Request'
