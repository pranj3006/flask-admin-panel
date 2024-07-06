"""
Controller for Healtcheck APIs
"""

import logging

from apps.core.utils import BaseResponseHandler
from apps.healthcheck.dtos import HealthcheckServiceDto
from apps.healthcheck.injectors import serv_healtcheck
from flask_restx import Resource

api = HealthcheckServiceDto.api
token_api = HealthcheckServiceDto.api
responseHandler = BaseResponseHandler()

@api.route("/all/")
class AllServicesHealthcheckController(Resource):
    """
    Controller to Healtcheck status of All Services
    """
    def __init__(self,api)-> None:
        super().__init__(self,api)

    @api.doc(validate=False)
    @api.expect()
    @api.response(
        HealthcheckServiceDto.serv_available_response_code,
        HealthcheckServiceDto.serv_available_response_message,
        HealthcheckServiceDto.resp_all_service_status,
    )
    @api.response(
        HealthcheckServiceDto.serv_unavailable_response_code,
        HealthcheckServiceDto.serv_unavailable_response_message,
        HealthcheckServiceDto.resp_all_service_status,
    )
    def get(self):
        """
        Perform healtcheck for all service
        Check if
        App is running
        DB is running
        """
        response = serv_healtcheck.get_all_services_status()
        if response["error_code"]!=0:
            return responseHandler.error_response(**response)
        return responseHandler.success_response(**response)


@api.route("/app/")
class AppServicesHealthcheckController(Resource):
    """
    Controller to Healtcheck status of App Service
    """
    def __init__(self,api)-> None:
        super().__init__(self,api)

    @api.doc(validate=False)
    @api.expect()
    @api.response(
        HealthcheckServiceDto.serv_available_response_code,
        HealthcheckServiceDto.serv_available_response_message,
        HealthcheckServiceDto.resp_service,
    )
    @api.response(
        HealthcheckServiceDto.serv_unavailable_response_code,
        HealthcheckServiceDto.serv_unavailable_response_message,
        HealthcheckServiceDto.resp_service,
    )
    def get(self):
        """
        Perform healtcheck for App service
        Check if
        App is running        
        """
        response = serv_healtcheck.get_app_status()
        if response["error_code"]!=0:
            return responseHandler.error_response(**response)
        return responseHandler.success_response(**response)
    

@api.route("/db/")
class DBServicesHealthcheckController(Resource):
    """
    Controller to Healtcheck status of DB Service
    """
    def __init__(self,api)-> None:
        super().__init__(self,api)

    @api.doc(validate=False)
    @api.expect()
    @api.response(
        HealthcheckServiceDto.serv_available_response_code,
        HealthcheckServiceDto.serv_available_response_message,
        HealthcheckServiceDto.resp_service,
    )
    @api.response(
        HealthcheckServiceDto.serv_unavailable_response_code,
        HealthcheckServiceDto.serv_unavailable_response_message,
        HealthcheckServiceDto.resp_service,
    )
    def get(self):
        """
        Perform healtcheck for DB service
        Check if
        DB is running        
        """
        response = serv_healtcheck.get_db_status()
        if response["error_code"]!=0:
            return responseHandler.error_response(**response)
        return responseHandler.success_response(**response)
    


@token_api.route("/token_db/")
class DBServicesHealthcheckTokenController(Resource):
    """
    Controller to Healtcheck status of DB Service
    """
    def __init__(self,api)-> None:
        super().__init__(self,api)

    @token_api.doc(validate=False)
    @token_api.expect()
    @token_api.response(
        HealthcheckServiceDto.serv_available_response_code,
        HealthcheckServiceDto.serv_available_response_message,
        HealthcheckServiceDto.resp_service,
    )
    @token_api.response(
        HealthcheckServiceDto.serv_unavailable_response_code,
        HealthcheckServiceDto.serv_unavailable_response_message,
        HealthcheckServiceDto.resp_service,
    )
    def get(self):
        """
        Perform healtcheck for DB service
        Check if
        DB is running        
        """
        response = serv_healtcheck.get_db_status()
        if response["error_code"]!=0:
            return responseHandler.error_response(**response)
        return responseHandler.success_response(**response)
    