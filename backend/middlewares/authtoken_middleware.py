import os
from flask import request
from apps.core.utils import BaseResponseHandler, verify_token
from flask_jwt_extended import decode_token, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from configs import API_SECRET_KEY

class AuthTokenMiddleware:

    def __init__(self) -> None:
        self.authorization_header = "Authorization"
        self.security_scheme = "ApiKeyAuth"
        self.authorizations = {
            self.security_scheme : { 
                "type":"apiKey",
                "in": "header",
                "name": self.authorization_header
            }
        }

        self.response_handler = BaseResponseHandler()
        self.env = os.getenv("FLASK_ENV","production")
        self.error_message = "Unauthorized Request"

    def check_token(self):
        """
        Validate Token
        """
        initial_check_results = self.check_swagger_and_header()
        if initial_check_results is not True:
            return initial_check_results
        
        token = request.headers[self.authorization_header].replace("Bearer ","")
        decoded_data,verify_error = verify_token(token)
        if verify_error:
            return self.response_handler.error_response(
                self.error_message, 403, f"Token Verification Failed: {verify_error}",403
            )

        if decoded_data and decoded_data.get("upn"):
            return self.process_decoded_data(decoded_data)
        
        return self.response_handler.error_response(
            self.error_message, 403, f"Token Verification Failed",403
        )
    
    def check_swagger_and_header(self):
        if request.path.endswith("swagger/") or request.path.endswith("swagger.json"):
            return None        
        if self.authorization_header not in request.headers:
            return self.response_handler.error_response(
            self.error_message, 401, f"No {self.authorization_header} Header Present",401
        )
        return True

    def process_decoded_data(self,decoded_data):
        user_email = decoded_data.get("upn")
        if "roles" not in decoded_data or len(decoded_data["roles"])!=1:
            return self.response_handler.error_response(
                self.error_message, 403, f"Missing or Invalid Roles",403
                )
        user_role = decoded_data.get("roles")[0]
        first_name = decoded_data.get("given_name")
        last_name = decoded_data.get("family_name")
        name = f"{first_name or ''} {last_name or ''}".strip()
        for attr in ["user_email","user_role","name"]:
            setattr(request,attr,locals()[attr])
        return None
    
    def check_email(self):
        initial_check_result = self.check_swagger_and_header()
        if initial_check_result is not True:
            return initial_check_result
        
        token = request.headers[self.authorization_header].replace("Bearer ","")
        try:
            user_email,role = headers.split("###")
        except ValueError:
            return self.response_handler.error_response(
            self.error_message, 401, f"The {self.authorization_header} header must be in format email###role",401
        )

        request.user_email=user_email
        request.user_role=role
        
        return None
    
    def verify_jwt(self):
        """
        Verifies JWT token using flask_jwt_extended's verify_jwt_in_request
        """
        initial_check_result = self.check_swagger_and_header()
        if initial_check_result is not True:
            return initial_check_result
        
        try:
            verify_jwt_in_request()
            return None
        except NoAuthorizationError:
            return self.response_handler.error_response(
                self.error_message, 401, f"Token is missing", 401
            )
        except (InvalidHeaderError):
            return self.response_handler.error_response(
                self.error_message, 401, f"Token is invalid or expired", 401
            )
        except Exception as e:
            return self.response_handler.error_response(
                self.error_message, 401, f"An error occurred: {str(e)}", 401
            )
        return None
        
    def verify_api_secret_key(self):
        """
        Verifies JWT token using flask_jwt_extended's verify_jwt_in_request
        """
        initial_check_result = self.check_swagger_and_header()        
        if initial_check_result is not True:            
            return initial_check_result
        
        token = request.headers[self.authorization_header].replace("Bearer ","")
        if token:
            if token!=API_SECRET_KEY:
                return self.response_handler.error_response(
                    self.error_message, 404, "Invalid API Key",401
                )
        else:
            return self.response_handler.error_response(
            self.error_message, 401, f"The {self.authorization_header} header must be in present",401
        )
        return None
    
    def middleware_method(self):
        return self.verify_api_secret_key()
    
mdw_authtoken = AuthTokenMiddleware()