"""
Healthcheck Service Interface
"""

from abc import ABC, abstractmethod

class IHealthcheckService(ABC):
    """
    Interface for Healthcheck Service
    """
    @abstractmethod
    def get_app_status(self)-> dict:
        """
        Check if App is running
        """
        pass

    @abstractmethod
    def get_db_status(self)-> dict:
        """
        Check if db is running
        """
        pass