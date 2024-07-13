"""
AdminPanel Controller for APIs
"""

import logging
from apps.flask_admin_panel.services import AdminPanelService
from apps.flask_admin_panel.middlewares.auth_utils import (
    authenticate_user,
    refresh_access_token,
)
from apps.flask_admin_panel.middlewares.base_response_handler import BaseResponseHandler
from flask import jsonify, make_response, render_template, request, redirect, url_for
from flask_restx import Resource, Api
from apps.flask_admin_panel.constant_config import PREFIX
from injector import inject

responseHander = BaseResponseHandler()


class AdminPanelIndexController(Resource):
    """Controller for Admin Panel Index"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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


class AdminPanelLoginPageController(Resource):
    """Controller for Admin Panel Login Page"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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


class AdminPanelLoginController(Resource):
    """Controller for Admin Panel Login"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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


class AdminPanelRefreshTokenController(Resource):
    """Controller for Admin Panel Refresh Token"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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


class AdminPanelListModelController(Resource):
    """Controller for Admin Panel List Models API"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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


class AdminPanelListRecordsController(Resource):
    """Controller for Admin Panel List Records for the model"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

    def get(self, model_name):
        """
        Get List of All Records of the model
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 2, type=int)
        paginated_records, lst_columns = self.serv_admin_panel.list_records(model_name, page, per_page)
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/list.html",
            model_name=model_name,
            records=paginated_records.items,
            columns=lst_columns,
            pagination=paginated_records
        )
        return make_response(html_content, 200, headers)


class AdminPanelEditRecordController(Resource):
    """Controller for Admin Panel Edit Record for the model"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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
                        "flask_admin_panel.admin_panel_list_records_controller",
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


class AdminPanelAddRecordController(Resource):
    """Controller for Admin Panel Add Record for the model"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

    def get(self, model_name):
        """
        Render form to Add a record
        """
        try:
            check, model_name, form = self.serv_admin_panel.add_record(
                request, model_name
            )
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
            check, model_name, form = self.serv_admin_panel.add_record(
                request, model_name
            )
            if check:

                return redirect(
                    url_for(
                        "flask_admin_panel.admin_panel_list_records_controller",
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


class AdminPanelDeleteRecordController(Resource):
    """Controller for Admin Panel Delete Record for the model"""

    @inject
    def __init__(
        self, admin_panel_api: Api, serv_admin_panel: AdminPanelService
    ) -> None:
        super().__init__()
        self.api = admin_panel_api
        self.serv_admin_panel = serv_admin_panel

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
                        "flask_admin_panel.admin_panel_list_records_controller",
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
