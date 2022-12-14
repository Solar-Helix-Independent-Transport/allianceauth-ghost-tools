from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
from corptools.models import EveLocation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from esi.models import Token


class GhostToolsConfiguration(models.Model):

    corporation = models.ForeignKey(
        EveCorporationInfo, null=True, default=None, blank=True, on_delete=models.CASCADE)

    stagings = models.ManyToManyField(EveLocation, blank=True)
    alliances = models.ManyToManyField(EveAllianceInfo, blank=True)

    def __str__(self):
        return "Configuration"

    def save(self, *args, **kwargs):
        if not self.pk and GhostToolsConfiguration.objects.exists():
            # Force a single object
            raise ValidationError(
                'Only one Settings Model is possible!')
        self.pk = self.id = 1  # If this happens to be deleted and recreated, force it to be 1
        return super().save(*args, **kwargs)

    class Meta:
        default_permissions = ()
        permissions = (
            ('access_ghost_tools', 'Can View Ghost Tools'),
        )


class GhostKickToken(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                related_name='ghost_character')
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
