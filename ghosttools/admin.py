from django.contrib import admin
from solo.admin import SingletonModelAdmin

from . import models


@admin.register(models.GhostToolsConfiguration)
class GhostToolsConfigurationAdmin(SingletonModelAdmin):
    filter_horizontal = ['corporations', 'stagings', 'alliances']
