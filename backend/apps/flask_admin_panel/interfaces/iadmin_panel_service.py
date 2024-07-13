"""
AdminPanel interface Class
"""

from abc import ABC, abstractmethod


class IAdminPanelService(ABC):
    """
    Interface for AdminPanel Class
    """

    @abstractmethod
    def register_model_for_admin_panel(self) -> dict:
        """Register a model for admin panel"""
        pass

    @abstractmethod
    def generate_model_form(self) -> dict:
        """Generate forms dynamically for each model"""
        pass

    @abstractmethod
    def generate_model_config(self) -> dict:
        """Generate model config"""
        pass

    @abstractmethod
    def regenerate_all_model_configs(self) -> dict:
        """ReGenerate all models configs"""
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """Get model info object"""
        pass

    @abstractmethod
    def list_records(self) -> dict:
        """List all the records of the model"""
        pass

    @abstractmethod
    def add_record(self) -> dict:
        """Add a record to the model"""
        pass

    @abstractmethod
    def edit_record(self) -> dict:
        """Edit Existing Record from the model"""
        pass

    @abstractmethod
    def delete_record(self) -> dict:
        """Delete the Records from the model"""
        pass
