from django.contrib import admin

from . import models


@admin.register(models.GhostToolsConfiguration)
class GhostToolsConfigurationAdmin(admin.ModelAdmin):
    filter_horizontal = ['stagings', 'alliances']
