import datetime
import os
from functools import wraps
from flask import current_app
from flask_admin_panel.middlewares.base_response_handler import BaseResponseHandler
from flask import make_response, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import InvalidHeaderError, NoAuthorizationError
from flask_admin_panel.constant_config import PREFIX


class AuthTokenMiddleware:
    excluded_paths = [
        PREFIX + "/admin_panel/admin_panel/page/login",
        PREFIX + "/admin_panel/admin_panel/login/",
        PREFIX + "/admin_panel/admin_panel/",
    ]

    def __init__(self) -> None:
        self.authorization_header = "Authorization"
        self.security_scheme = "ApiKeyAuth"
        self.authorizations = {
            self.security_scheme: {
                "type": "apiKey",
                "in": "header",
                "name": self.authorization_header,
            }
        }

        self.ADMIN_PANEL_API_SECRET_KEY = os.getenv("ADMIN_PANEL_API_SECRET_KEY")
        self.response_handler = BaseResponseHandler()
        self.env = os.getenv("FLASK_ENV", "production")
        self.error_message = "Unauthorized Request"

    def check_swagger_and_header(self):
        if request.path.endswith("swagger/") or request.path.endswith("swagger.json"):
            return None
        if self.authorization_header not in request.headers:
            return self.response_handler.error_response(
                self.error_message,
                401,
                f"No {self.authorization_header} Header Present",
                401,
            )
        return True

    def check_exclude(self):
        if request.path in self.excluded_paths:
            return None
        return True

    def check_for_login(self):
        if request.path.endswith("admin_panel/login"):
            return True
        return False

    def check_for_admin_panel(self):
        if request.path.find(PREFIX + "/admin_panel/admin_panel/") > 0:
            return self.check_exclude()
        return False

    def verify_jwt(self):
        """
        Verifies JWT token using flask_jwt_extended's verify_jwt_in_request
        """
        if self.check_for_admin_panel():
            try:
                verify_jwt_in_request()
                return None
            except NoAuthorizationError:
                return self.response_handler.error_response(
                    self.error_message, 401, f"Token is missing", 401
                )
            except InvalidHeaderError:
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

        token = request.headers[self.authorization_header].replace("ApiKey ", "")
        if token:
            if token != self.ADMIN_PANEL_API_SECRET_KEY:
                return self.response_handler.error_response(
                    self.error_message, 404, "Invalid API Key", 401
                )
        else:
            return self.response_handler.error_response(
                self.error_message,
                401,
                f"The {self.authorization_header} header must be in present",
                401,
            )
        return None

    def middleware_method(self):
        if current_app.config.get("TESTING"):
            return
        return self.verify_jwt()

    @classmethod
    def exclude(cls, paths):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(paths)
                print(request.path)
                if request.path in paths:
                    return func(*args, **kwargs)
                return cls.middleware_method() or func(*args, **kwargs)

            return wrapper

        return decorator


mdw_authtoken = AuthTokenMiddleware()
