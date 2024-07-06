"""
Healthcheck Service Class
"""

import logging
from apps.healthcheck.interfaces import IHealthcheckService
from extensions import db
from sqlalchemy import text

class HealthcheckService(IHealthcheckService):
    """
    Service class for Healthchecks
    """
    def __init__(self) -> None:
        """
        Initialze class variables
        """
        self._app_status:dict = {
            "status": 200,
            "message": "App Running",
            "data": "",
            "error_code":0,
            "error_details":""
        }

        self._db_status:dict = {
            "status": 200,
            "message": "DB Running",
            "data": "",
            "error_code":0,
            "error_details":""
        }

        self._all_status:dict = {
            "status": 200,
            "message": "All Sevices Running",
            "data": {"services":[]},
            "error_code":0,
            "error_details":""
        }

    def get_app_status(self) -> dict:
        """
        Get App Status to check if its running
        """
        logging.info("App is running")
        return self._app_status
    
    def get_db_status(self) -> dict:
        """
        Check DB connection to check if App is able to connect to DB
        """
        try:
            db.session.execute(text('SELECT 1'))
            logging.info("DB is running")
        except Exception as exc:
            self._db_status = {
            "status": 503,
            "message": "DB Not Available or Unable to Connect",
            "data": "",
            "error_code":2,
            "error_details":str(exc)
            }
            logging.critical("DB is NOT Available")
            logging.error("DB Connection Error %s",exc)
        return self._db_status
    
    def get_all_services_status(self) -> dict:
        """
        Check status of all services
        """
        lst_service_status:list = []
        lst_service_status.append(self.get_app_status())
        lst_service_status.append(self.get_db_status())

        for service_status in lst_service_status:
            if service_status["error_code"] != 0:
                self._all_status["error_code"] = 1
            self._all_status["data"]["services"].append(service_status)

        if self._all_status["error_code"]!= 0:
            self._all_status["status"] = 503
            self._all_status["Message"] = "One or more services are not available"
            logging.critical("One of more services are  NOT Available")
            
        return self._all_status