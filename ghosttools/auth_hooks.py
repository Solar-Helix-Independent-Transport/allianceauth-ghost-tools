from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import gettext_lazy as _

from . import urls


class GhostDash(MenuItemHook):
    def __init__(self):

        MenuItemHook.__init__(self,
                              "Ghost Tools",
                              'fas fa-ghost fa-fw',
                              'ghosttools:view',
                              navactive=['ghosttools:'])

    def render(self, request):
        if request.user.has_perm('ghosttools.access_ghost_tools'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return GhostDash()


@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'ghosttools', r'^ghosts/')
