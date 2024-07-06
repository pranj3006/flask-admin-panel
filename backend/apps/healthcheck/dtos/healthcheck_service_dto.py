"""
DTOs for Healtcheck
"""
from flask_restx import Namespace, fields

class HealthcheckServiceDto:
    """
    Healtcheck DTO Definition
    """

    api = Namespace("healthcheck",description="Healtcheck status of all service")
    resp_service = api.model(
        "Service Healtcheck Status",
        {
            "status": fields.Integer,
            "message": fields.String,
            "data": fields.String,
            "error_code": fields.Integer,
            "error_details": fields.String,
        }
    )

    service = api.model(
        "Services Object",
        {
            "services": fields.List(fields.Nested(resp_service)),            
        }
    )

    resp_all_service_status = api.model(
        "All Services Healtcheck Status",
        {
            "status": fields.Integer,
            "message": fields.String,
            "data": fields.Nested(service),
            "error_code": fields.Integer,
            "error_details": fields.String,
        }
    )

    serv_available_response_code = 200
    serv_available_response_message = "Service Available"

    serv_unavailable_response_code = 503
    serv_unavailable_response_message = "Service Unavailable"
