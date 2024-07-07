"""
AdminPanel Controller for APIs
"""

import logging

from flask_admin_panel.dtos import AdminPanelDto
# from flask_admin_panel.injectors import serv_admin_panel
from flask_admin_panel.middlewares.auth_utils import (
    authenticate_user,
    refresh_access_token,
)
from flask_admin_panel.middlewares.base_response_handler import BaseResponseHandler
from flask import jsonify, make_response, redirect, render_template, request, url_for
from flask_restx import Resource
from flask_admin_panel.constant_config import PREFIX
from flask import current_app
api = AdminPanelDto.api
responseHander = BaseResponseHandler()

@api.route("/")
class AdminPanelIndexController(Resource):
    """Controller for Admin Panel Index"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]
    def get(self):
        """
        Authenticate User and Generate Token
        """
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/index.html",
            app_title=self.serv_admin_panel.app_title,
            api_url_prefix=PREFIX,
        )
        return make_response(html_content, 200, headers)


@api.route("/page/login")
class AdminPanelLoginPangeController(Resource):
    """Controller for Admin Panel Login Page"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]


    def get(self):
        """
        Authenticate User and Generate Token
        """
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/login.html",
            app_title=self.serv_admin_panel.app_title,
            api_url_prefix=PREFIX,
        )
        return make_response(html_content, 200, headers)


@api.route("/login/")
class AdminPanelLoginController(Resource):
    """Controller for Admin Panel Login"""

    def __init__(self, api) -> None:
        super().__init__(self, api)

    def post(self):
        """
        Authenticate User and Generate Token
        """
        auth = request.json
        if not auth or not auth.get("username") or not auth.get("password"):
            return make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm="Login required!"'},
            )

        access_token, refresh_token = authenticate_user(request)
        if access_token:
            return jsonify(
                {"access_token": access_token, "refresh_token": refresh_token}
            )
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )


@api.route("/refresh_token/")
class AdminPanelRefreshTokenController(Resource):
    """Controller for Admin Panel Refresh Token"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        

    def post(self):
        """
        Authenticate User and Generate new Access Token using Refresh Token
        """

        access_token = refresh_access_token(request)
        if access_token:
            return jsonify({"access_token": access_token})
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )


@api.route("/list_models/")
class AdminPanelListModelController(Resource):
    """Controller for Admin Panel List Models API"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]

    def get(self):
        """
        Get List of All Models
        """
        lst_models = list(self.serv_admin_panel.models_for_admin_panel.keys())
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/models_list.html",
            app_title=self.serv_admin_panel.app_title,
            models=lst_models,
        )
        return make_response(html_content, 200, headers)


@api.route("/list_records/<model_name>/")
class AdminPanelListRecordsController(Resource):
    """Controller for Admin Panel List Records for the model"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]

    def get(self, model_name):
        """
        Get List of All Records of the model
        """
        lst_records, lst_columns = self.serv_admin_panel.list_records(model_name)
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/list.html",
            model_name=model_name,
            records=lst_records,
            columns=lst_columns,
        )
        return make_response(html_content, 200, headers)


@api.route("/<model_name>/edit_record/<int:id>", methods=["GET", "POST"])
class AdminPanelEditRecordController(Resource):
    """Controller for Admin Panel Edit Record for the model"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]

    def get(self, model_name, id):
        """
        Render form to edit a record
        """
        try:
            check, model_name, form = self.serv_admin_panel.edit_record(
                request, model_name, id
            )
            headers = {"Content-Type": "text/html"}
            html_content = render_template(
                "flask_admin_panel/form.html",
                model_name=model_name,
                form=form,
                action="edit",
                record_id=id,
            )
            return make_response(html_content, 200, headers)
        except Exception as e:
            logging.error(f"Error fetching record {id} for editing: {str(e)}")
            return {"message": f"Error fetching record {id} for editing"}, 500

    def post(self, model_name, id):
        """
        Update an existing record
        """
        try:
            check, model_name, form = self.serv_admin_panel.edit_record(
                request, model_name, id
            )
            if check:
                return redirect(
                    url_for(
                        "flask_admin_panel.admin_panel_admin_panel_list_records_controller",
                        model_name=model_name,
                    )
                )
            else:
                headers = {"Content-Type": "text/html"}
                html_content = render_template(
                    "flask_admin_panel/form.html",
                    model_name=model_name,
                    form=form,
                    action="edit",
                    record_id=id,
                )
                return make_response(html_content, 400, headers)
        except Exception as e:
            logging.error(
                f"Error updating record {id} for model {model_name}: {str(e)}"
            )
            return {
                "message": f"Error updating record {id} for model {model_name}"
            }, 500


@api.route("/add_record/<model_name>/", methods=["GET", "POST"])
class AdminPanelAddRecordController(Resource):
    """Controller for Admin Panel Add Record for the model"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]

    def get(self, model_name):
        """
        Render form to Add a record
        """
        try:
            check, model_name, form = self.serv_admin_panel.add_record(request, model_name)
            headers = {"Content-Type": "text/html"}
            html_content = render_template(
                "flask_admin_panel/form.html",
                model_name=model_name,
                form=form,
            )
            return make_response(html_content, 200, headers)
        except Exception as e:
            logging.error(f"Error rendering add form for model {model_name}: {str(e)}")
            return {"message": f"Error rendering add form for model {model_name}"}, 500

    def post(self, model_name):
        """
        Add a record
        """
        try:
            check, model_name, form = self.serv_admin_panel.add_record(request, model_name)
            if check:

                return redirect(
                    url_for(
                        "flask_admin_panel.admin_panel_admin_panel_list_records_controller",
                        model_name=model_name,
                    )
                )
            else:
                headers = {"Content-Type": "text/html"}
                html_content = render_template(
                    "flask_admin_panel/form.html",
                    model_name=model_name,
                    form=form,
                )
                return make_response(html_content, 400, headers)
        except Exception as e:
            logging.error(f"Error adding record for model {model_name}: {str(e)}")
            return {"message": f"Error adding record for model {model_name}"}, 500


@api.route("/<model_name>/delete_record/<int:id>", methods=["POST"])
class AdminPanelDeleteRecordController(Resource):
    """Controller for Admin Panel Delete Record for the model"""

    def __init__(self, api) -> None:
        super().__init__(self, api)
        self.serv_admin_panel = current_app.extensions["flask_admin_panel"]

    def post(self, model_name, id):
        """
        Delete an existing record
        """
        try:
            check, model_name, form = self.serv_admin_panel.delete_record(
                request, model_name, id
            )
            if check:
                return redirect(
                    url_for(
                        "flask_admin_panel.admin_panel_admin_panel_list_records_controller",
                        model_name=model_name,
                    )
                )

        except Exception as e:
            logging.error(
                f"Error updating record {id} for model {model_name}: {str(e)}"
            )
            return {
                "message": f"Error updating record {id} for model {model_name}"
            }, 500