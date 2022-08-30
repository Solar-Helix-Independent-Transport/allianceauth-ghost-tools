import logging

from allianceauth.eveonline.models import EveCharacter
from corptools.models import EveItemType, EveLocation
from corptools.providers import esi
from corptools.task_helpers.corp_helpers import get_corp_token
from django.conf import settings
from ninja import NinjaAPI
from ninja.responses import codes_4xx
from ninja.security import django_auth

from . import models

logger = logging.getLogger(__name__)


api = NinjaAPI(title="Ghost Tools API", version="0.0.1",
               urls_namespace='ghosttools:api', auth=django_auth, csrf=True,)
# openapi_url=settings.DEBUG and "/openapi.json" or "")


@api.get(
    "ghost/list",
    tags=["Ghosts"]
)
def get_ghost_list(request):
    if request.user.has_perm('ghosttools.access_ghost_tools'):
        # Get Corp ID
        cid = models.GhostToolsConfiguration.objects.get(
            id=1).corporation.corporation_id

        # find a corp token
        token = get_corp_token(
            cid, ['esi-corporations.track_members.v1'], ['Director'])

        # grab member tracking list
        tracking = esi.client.Corporation.get_corporations_corporation_id_membertracking(
            corporation_id=cid,
            token=token.valid_access_token()).result()

        # get all characters in auth
        location_ids = []
        type_ids = []
        char_id = {}
        for c in tracking:
            char_id[c['character_id']] = {
                "char": {
                    "id": c.get("character_id", 0),
                    "name": "**UNKNOWN**"},
                "main": {
                    "id": 0,
                    "name": "**ORPHAN**",
                    "corp": "**UNKNOWN**",
                    "alli": "**UNKNOWN**"
                },
                "location": {
                    "id": c.get("location_id", 0),
                    "name": "",
                    "system": {"id": 0, "name": ""}
                },
                "ship": {
                    "id": c.get("ship_type_id", ""),
                    "name": ""
                },
                "last_clone_jump_date": "",
                "last_station_change_date": "",
                "death_clone": {
                    "id": 0,
                    "name": ""
                },
                "logoff_date": c.get("logoff_date", ""),
                "start_date": c.get("start_date", "")
            }
            location_ids.append(c.get("location_id", ""))
            type_ids.append(c.get("ship_type_id", ""))

        c_models = EveCharacter.objects.filter(
            character_id__in=list(char_id.keys())
        ).select_related(
            "character_ownership",
            "character_ownership__user",
            "character_ownership__user__profile",
            "character_ownership__user__profile__main_character",
            "characteraudit",
            "characteraudit__clone",
            "characteraudit__clone__location_name",
        )
        for c in c_models:
            char_id[c.character_id]["char"] = {
                "id": c.character_id,
                "name": c.character_name
            }
            try:
                char_id[c.character_id]["main"] = {
                    "id": c.character_ownership.user.profile.main_character.character_id,
                    "name": c.character_ownership.user.profile.main_character.character_name,
                    "corp": c.character_ownership.user.profile.main_character.corporation_name,
                    "alli": c.character_ownership.user.profile.main_character.alliance_name,
                }
            except Exception as e:
                print(e)
                pass
            try:
                char_id[c.character_id]["death_clone"] = {
                    "id": c.characteraudit.clone.location_name.location_id,
                    "name": c.characteraudit.clone.location_name.location_name
                }
            except Exception as e:
                pass
            try:
                char_id[c.character_id]["last_station_change_date"] = c.characteraudit.clone.last_station_change_date
            except Exception as e:
                pass
            try:
                char_id[c.character_id]["last_clone_jump_date"] = c.characteraudit.clone.last_clone_jump_date
            except Exception as e:
                pass
        locations = EveLocation.objects.filter(location_id__in=location_ids)
        loc_dict = {}
        for l in locations:
            loc_dict[l.location_id] = l.location_name

        types = EveItemType.objects.filter(type_id__in=type_ids)
        type_dict = {}
        for t in types:
            type_dict[t.type_id] = t.name

        for id, d in char_id.items():
            d["location"]['name'] = loc_dict.get(
                d['location']['id'], f"Unknown {d['location']['id']}")
            d["ship"]['name'] = type_dict.get(
                d['ship']['id'], f"Unknown {d['ship']['id']}")

        return list(char_id.values())
    else:
        return []


@api.post(
    "ghost/kick",
    tags=["Ghosts"]
)
def get_ghost_list(request, character_id: int):
    if not request.user.has_perm('ghosttools.access_ghost_tools'):
        return 403, "Permission Denied"

    try:
        if id:
            linked = request.user.ghost_character
            if linked:
                online = esi.client.Location.get_characters_character_id_online(
                    character_id=linked.token.character_id, token=linked.token.valid_access_token()).result()
                if online.get('online', False):
                    esi.client.User_Interface.post_ui_openwindow_information(
                        target_id=character_id, token=linked.token.valid_access_token()).result()

        return 200, "Sent Open Request"
    except Exception as e:
        print(e)
        return 200, "Failed to Send Open Request"
