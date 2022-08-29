from django.apps import AppConfig
from . import __version__


class GhostToolsConfig(AppConfig):
    name = 'ghosttools'
    label = 'ghosttools'

    verbose_name = f"Init Ghost Tools v{__version__}"
