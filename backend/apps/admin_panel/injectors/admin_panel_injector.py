"""
AdminPanel Injector Class definition
"""

from apps.admin_panel.services import AdminPanelService
from injector import Binder, Injector, Module, singleton


class AdminPanelModule(Module):
    """
    AdminPanel Injector Class definition
    """

    def configure(self, binder: Binder) -> None:

        binder.bind(AdminPanelService, to=AdminPanelService, scope=singleton)


injector = Injector([AdminPanelModule()])
serv_admin_panel = injector.get(AdminPanelService)