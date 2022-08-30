from django.contrib import admin

from . import models


@admin.register(models.GhostToolsConfiguration)
class GhostToolsConfigurationAdmin(admin.ModelAdmin):
    pass
