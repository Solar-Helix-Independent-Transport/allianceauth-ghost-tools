import logging

from allianceauth.eveonline.models import EveCharacter
from corptools.models import EveItemType, EveLocation
from corptools.providers import esi_openapi
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect, render
from esi.decorators import token_required
from esi.models import Token

from .models import GhostKickToken, GhostToolsConfiguration

logger = logging.getLogger(__name__)

_TRACKING_SCOPES = [
    'esi-corporations.track_members.v1',
    'esi-characters.read_corporation_roles.v1',
]


def _has_director_role(token):
    """Return True if the token character holds the Director role. Cached 5 min."""
    cache_key = f'ghosttools_director_{token.character_id}_{token.pk}'
    result = cache.get(cache_key)
    if result is not None:
        return result
    try:
        roles = esi_openapi.client.Character.GetCharactersCharacterIdRoles(
            character_id=token.character_id,
            token=token,
        ).result(use_etag=False, use_cache=True)
        result = 'Director' in (roles.roles or [])
    except Exception:
        result = False
    cache.set(cache_key, result, 300)
    return result


def _get_corp_options():
    """
    Return a dict keyed by corp_id of the first Director-role token found for
    each configured corporation. Any token in the DB qualifies regardless of
    which user added it.

    Each value: {token, token_id, character_id, char_name, corp_id, corp_name}
    """
    config = GhostToolsConfiguration.get_solo()
    configured_corp_ids = set(
        config.corporations.values_list('corporation_id', flat=True)
    )

    char_ids = list(
        EveCharacter.objects.filter(
            corporation_id__in=configured_corp_ids
        ).values_list('character_id', flat=True)
    )

    tokens = Token.objects.filter(
        character_id__in=char_ids,
    ).require_scopes(_TRACKING_SCOPES)

    char_lookup = {
        c.character_id: c
        for c in EveCharacter.objects.filter(
            character_id__in=tokens.values_list('character_id', flat=True)
        )
    }

    corps = {}
    for token in tokens:
        char = char_lookup.get(token.character_id)
        if not char:
            continue
        corp_id = char.corporation_id
        if corp_id in corps:
            continue  # already have a verified director token for this corp
        if _has_director_role(token):
            corps[corp_id] = {
                'token': token,
                'token_id': token.pk,
                'character_id': token.character_id,
                'char_name': char.character_name,
                'corp_id': corp_id,
                'corp_name': char.corporation_name,
            }

    return corps, config


@login_required
@permission_required('ghosttools.access_ghost_tools')
def main_view(request):
    corp_options, _ = _get_corp_options()

    token_id = request.session.get('ghosttools_token_id')
    token = None

    if token_id:
        for opt in corp_options.values():
            if opt['token_id'] == token_id:
                token = opt['token']
                break

    if not token:
        if len(corp_options) == 1:
            opt = next(iter(corp_options.values()))
            token = opt['token']
            request.session['ghosttools_token_id'] = token.pk
        else:
            return redirect('ghosttools:select_corp')

    return _render_dashboard(request, token)


def _build_member_data(token, config):
    """Fetch ESI member tracking and enrich from Auth DB."""
    char = EveCharacter.objects.filter(character_id=token.character_id).first()
    if not char:
        raise ValueError(f'Character {token.character_id} not found in Auth')
    corp_id = char.corporation_id
    corp_name = char.corporation_name

    tracking = esi_openapi.client.Corporation.GetCorporationsCorporationIdMembertracking(
        corporation_id=corp_id,
        token=token,
    ).result(use_etag=False)

    alliance_ids = set(config.alliances.values_list('alliance_id', flat=True))
    valid_states = {'Member', 's_vip'}

    char_map = {}
    location_ids = []
    type_ids = []

    for c in tracking:
        char_map[c.character_id] = {
            'char_id': c.character_id,
            'char_name': '',
            'main_id': 0,
            'main_name': '',
            'corp_name': '',
            'corp_id': '',
            'alliance_name': '',
            'alliance_id': 0,
            'state': '',
            'location_id': c.location_id,
            'location_name': '',
            'ship_id': c.ship_type_id,
            'ship_name': '',
            'death_clone': '',
            'logoff_date': c.logoff_date,
            'start_date': c.start_date,
            'is_orphan': True,
        }
        location_ids.append(c.location_id)
        type_ids.append(c.ship_type_id)

    c_models = EveCharacter.objects.filter(
        character_id__in=char_map.keys()
    ).select_related(
        'character_ownership__user__profile__state',
        'character_ownership__user__profile__main_character',
        'characteraudit__clone__location_name',
    )

    for c in c_models:
        d = char_map[c.character_id]
        d['char_name'] = c.character_name
        try:
            profile = c.character_ownership.user.profile
            main = profile.main_character
            state = profile.state.name
            d.update({
                'main_id': main.character_id,
                'main_name': main.character_name,
                'corp_name': main.corporation_name,
                'corp_id': main.corporation_id,
                'alliance_name': main.alliance_name or '',
                'alliance_id': main.alliance_id or 0,
                'state': state,
                'is_orphan': (
                    (main.alliance_id not in alliance_ids) or
                    (state not in valid_states)
                ),
            })
        except Exception:
            pass
        try:
            d['death_clone'] = c.characteraudit.clone.location_name.location_name
        except Exception:
            pass

    # Bulk name lookup for characters not registered in Auth (public ESI endpoint,
    # no token required, max 1000 IDs per call).
    unknown_ids = [cid for cid, d in char_map.items() if not d['char_name']]
    for i in range(0, len(unknown_ids), 1000):
        try:
            results = esi_openapi.client.Universe.PostUniverseNames(
                body=unknown_ids[i:i + 1000]
            ).result()
            for entry in results:
                if entry.category == 'character' and entry.id in char_map:
                    char_map[entry.id]['char_name'] = entry.name
        except Exception as e:
            logger.warning('ESI bulk name lookup failed for batch starting at index %d: %s', i, str(e))

    loc_dict = {
        loc.location_id: loc.location_name
        for loc in EveLocation.objects.filter(location_id__in=location_ids)
    }
    type_dict = {
        t.type_id: t.name
        for t in EveItemType.objects.filter(type_id__in=type_ids)
    }

    members = []
    for d in char_map.values():
        d['location_name'] = loc_dict.get(d['location_id'], f"Unknown ({d['location_id']})")
        d['ship_name'] = type_dict.get(d['ship_id'], f"Unknown ({d['ship_id']})")
        members.append(d)

    members.sort(key=lambda x: x['char_name'] or '')
    return members, corp_id, corp_name


def _render_dashboard(request, token):
    config = GhostToolsConfiguration.get_solo()
    error = None
    members = []
    corp_id = None
    corp_name = 'Unknown'

    try:
        members, corp_id, corp_name = _build_member_data(token, config)
    except Exception:
        logger.exception('Ghost Tools dashboard fetch error')
        error = 'Failed to load member tracking data. The token may be invalid or the character may have lost Director role.'

    try:
        ghost_char = request.user.ghost_character.token.character_name
    except Exception:
        ghost_char = None

    return render(request, 'ghosttools/dashboard.html', {
        'page_title': 'Ghost Tools',
        'members': members,
        'stagings': list(config.stagings.values_list('location_name', flat=True)),
        'token': token,
        'corp_id': corp_id,
        'corp_name': corp_name,
        'error': error,
        'ghost_char': ghost_char,
        'member_count': len(members),
    })


@login_required
@permission_required('ghosttools.access_ghost_tools')
def select_corp(request):
    corp_options, _ = _get_corp_options()

    if request.method == 'POST':
        try:
            token_id = int(request.POST.get('token_id', 0))
        except (TypeError, ValueError):
            token_id = 0

        valid_token_ids = {opt['token_id'] for opt in corp_options.values()}
        if token_id and token_id in valid_token_ids:
            request.session['ghosttools_token_id'] = token_id
            return redirect('ghosttools:view')
        messages.error(request, 'Invalid corporation selection.')

    return render(request, 'ghosttools/select_corp.html', {
        'page_title': 'Ghost Tools - Select Corporation',
        'corp_options': list(corp_options.values()),
    })


@login_required
@permission_required('ghosttools.access_ghost_tools')
def kick_character(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        character_id = int(request.POST.get('character_id', 0))
        if not character_id:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid character_id'}, status=400)

    try:
        linked = request.user.ghost_character
    except GhostKickToken.DoesNotExist:
        return JsonResponse({'status': 'no_ghost_char'}, status=400)

    try:
        online = esi_openapi.client.Location.GetCharactersCharacterIdOnline(
            character_id=linked.token.character_id,
            token=linked.token,
        ).result(use_etag=False)
        if not online.online:
            return JsonResponse({'status': 'offline'})
        esi_openapi.client.User_Interface.PostUiOpenwindowInformation(
            target_id=character_id,
            token=linked.token,
        ).result()
        return JsonResponse({'status': 'sent'})
    except Exception as e:
        logger.error('Ghost kick error: %s', e)
        return JsonResponse({'status': 'failed'})


@login_required
@permission_required('ghosttools.access_ghost_tools')
@token_required(scopes=_TRACKING_SCOPES)
def ghost_corp_add(request, token):
    return redirect('ghosttools:view')


@login_required
@permission_required('ghosttools.access_ghost_tools')
@token_required(scopes=['esi-ui.open_window.v1', 'esi-location.read_online.v1'])
def ghost_setkick_character(request, token):
    if token:
        try:
            link = GhostKickToken.objects.get(user=request.user)
            link.token = token
            link.save()
        except GhostKickToken.DoesNotExist:
            GhostKickToken.objects.create(user=request.user, token=token)
        messages.success(request, f'Linked Ghost Character: {token.character_name}')
    return redirect('ghosttools:view')
