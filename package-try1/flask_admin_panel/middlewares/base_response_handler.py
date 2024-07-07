"""
Base Response handler for API responses
"""

from datetime import datetime

from flask import jsonify
from flask_restx import Resource


class BaseResponseHandler(Resource):
    """
    Class for Base Response Handler
    """

    def _convert_datetime(self, obj):
        """
        Convert datetime objects in the dictionary to strings.
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, datetime):
                    obj[key] = value.isoformat()
                elif isinstance(value, list):
                    obj[key] = [self._convert_datetime(item) for item in value]
                elif isinstance(value, dict):
                    obj[key] = self._convert_datetime(value)
        elif isinstance(obj, list):
            obj = [self._convert_datetime(item) for item in obj]
        return obj

    def success_response(self, status, message, data, pagination=None, **rest):
        """
        Response structure on success
        """
        response_object = {
            "status": status,
            "message": message,
            "data": data,
            "pagination": pagination,
            **rest,
        }
        response_object = self._convert_datetime(response_object)

        # Create the JSON response
        response = jsonify(response_object)

        # Set the status code
        response.status_code = status

        return response

    def validation_error_response(self, errors, status=422):
        """
        Response structure on validation error
        """
        response_object = {"status": status, "errors": errors}
        return response_object, status

    def error_response(self, message, error_code, error_details, status=400, **rest):
        """
        Response structure on error
        """
        err_object = {
            "status": status,
            "message": message,
            "error_code": error_code,
            "error_details": error_details,
            **rest,
        }
        return err_object, status

    def internal_err_resp(self):
        """
        Response structure on internall error
        """
        err_object = {
            "status": 500,
            "message": "Something went wrong during the process!",
        }
        err_object["error_reason"] = "server_error"
        return err_object, 500

    def dump_schema_on_arr(self, schema, arr):
        """
        Response structure on dump schema
        """
        schema_ = schema(many=True)
        return schema_.dump(arr)

    def dump_schema_on_obj(self, schema, obj):
        """
        Response structure on obj schema
        """
        resp = schema().dump(obj)
        return resp

    def get_pagination(self, arr):
        """
        Response structure for pagination
        """
        pagination = {"page": arr.page, "per_page": arr.per_page, "total": arr.total}
        return pagination