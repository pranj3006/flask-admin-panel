"""
Base Response handler for API responses
"""
from flask_restx import Resource


class BaseResponseHandler(Resource):
    """
    Class for Base Response Handler
    """
    def success_response(self,status,message,data,pagination=None,**rest):
        """
        Response structure on success
        """
        response_object = {
                "status": status, 
                "message": message,
                "data":data,
                "pagination":pagination,
                **rest
            }
        return response_object,status

    def validation_error_response(self,errors,status=422):
        """
        Response structure on validation error
        """
        response_object = {"status": status, "errors": errors}
        return response_object,status

    def error_response(self,message,error_code, error_details,status=400,**rest):
        """
        Response structure on error
        """
        err_object = {
            "status": status, 
            "message": message,
            "error_code": error_code,
            "error_details": error_details,
            **rest
            }
        return err_object,status

    def internal_err_resp(self):
        """
        Response structure on internall error
        """
        err_object = {"status": 500, "message": "Something went wrong during the process!"}
        err_object["error_reason"] = "server_error"
        return err_object, 500

    def dump_schema_on_arr(self,schema,arr):
        """
        Response structure on dump schema
        """
        schema_ = schema(many=True)
        return schema_.dump(arr)

    def dump_schema_on_obj(self,schema,obj):
        """
        Response structure on obj schema
        """
        resp = schema().dump(obj)
        return resp

    def get_pagination(self,arr):
        """
        Response structure for pagination
        """
        pagination = {
            "page":arr.page,
            "per_page":arr.per_page,
            "total":arr.total
        }
        return pagination