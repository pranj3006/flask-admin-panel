"""
Healthcheck Injector class 
"""

from apps.healthcheck.services import HealthcheckService
from injector import Module,singleton,Injector

class HealthcheckServiceInjector(Module):
    """
    Healthcheck Injector class 
    """

    def configure(self,binder):
        """
        Define the configuration for binding services
        """
        binder.bind(HealthcheckService,to=HealthcheckService,scope=singleton)

injector = Injector([HealthcheckServiceInjector()])

serv_healtcheck = injector.get(HealthcheckService)