from allianceauth.eveonline.models import EveCharacter
from corptools.models import EveItemType, EveLocation
from ninja import NinjaAPI
from ninja.security import django_auth
from ninja.responses import codes_4xx

from corptools.providers import esi
from corptools.task_helpers.corp_helpers import get_corp_token
from django.conf import settings
from . import models


import logging

logger = logging.getLogger(__name__)


api = NinjaAPI(title="Ghost Tools API", version="0.0.1",
               urls_namespace='ghosttools:api', auth=django_auth, csrf=True,)
               #openapi_url=settings.DEBUG and "/openapi.json" or "")


@api.get(
    "ghost/list",
    tags=["Ghosts"]
)
def get_ghost_list(request):
    if request.user.has_perm('ghosttools.access_ghost_tools'):
        # Get Corp ID
        cid = models.GhostToolsConfiguration.objects.get(id=1).corporation.corporation_id
        
        # find a corp token
        token = get_corp_token(cid, ['esi-corporations.track_members.v1'], ['Director'])

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
                "char_name": "",
                "main_name": "",
                "location": "",
                "ship": "",
                "location_id": c.get("location_id", ""),
                "last_clone_jump_date": "",
                "last_station_change_date": "",
                "death_clone": "",
                "logoff_date": c.get("logoff_date", ""),
                "start_date":  c.get("start_date", ""),
                "ship_type_id":  c.get("ship_type_id", ""),
            }
            location_ids.append(c.get("location_id", ""))
            type_ids.append(c.get("ship_type_id", ""))
        
        c_models = EveCharacter.objects.filter(character_id__in=list(char_id.keys()))
        for c in c_models:
            char_id[c.character_id]["char_name"]=c.character_name
            try:
                char_id[c.character_id]["main_name"]=c.character_ownership.user.profile.main_character.character_name
            except Exception as e:
                print(e)
                pass
            try:
                char_id[c.character_id]["death_clone"]=c.characteraudit.clone.location_name.location_name
            except Exception as e:
                pass
            try:
                char_id[c.character_id]["last_station_change_date"]=c.characteraudit.clone.last_station_change_date
            except Exception as e:
                pass
            try:
                char_id[c.character_id]["last_clone_jump_date"]=c.characteraudit.clone.last_clone_jump_date
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
            d["location"] = loc_dict.get(d['location_id'], "")
            d["ship"] = type_dict.get(d['ship_type_id'], "")
        
        return list(char_id.values())
    else:
        return []
