from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
from corptools.models import EveLocation
from django.contrib.auth.models import User
from django.db import models
from esi.models import Token
from solo.models import SingletonModel


class GhostToolsConfiguration(SingletonModel):
    corporations = models.ManyToManyField(EveCorporationInfo, blank=True)
    stagings = models.ManyToManyField(EveLocation, blank=True)
    alliances = models.ManyToManyField(EveAllianceInfo, blank=True)

    def __str__(self):
        return "Ghost Tools Configuration"

    class Meta:
        default_permissions = ()
        permissions = (
            ('access_ghost_tools', 'Can View Ghost Tools'),
        )


class GhostKickToken(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='ghost_character',
    )
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
