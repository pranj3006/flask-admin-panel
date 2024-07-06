from apps.healthcheck.controllers import healthcheck_ns,healthcheck_token_ns
from flask import Blueprint
from flask_restx import Api
from middlewares import mdw_authtoken

healthcheck_bp = Blueprint("healthcheck",__name__)

healthcheck_token_bp = Blueprint("healthchecktoken",__name__)
healthcheck_token_bp.before_request(mdw_authtoken.middleware_method)


healthcheck_api = Api(healthcheck_bp,
                      title = "Healthcheck",
                      description="Healthcheck status for services",
                      doc="/swagger/")


healthcheck_token_api = Api(healthcheck_token_bp,
                        title = "Healthcheck",
                        description="Healthcheck status for services",
                        doc="/swagger/",
                        authorizations=mdw_authtoken.authorizations,
                        security=[mdw_authtoken.security_scheme])

healthcheck_api.add_namespace(healthcheck_ns)
healthcheck_token_api.add_namespace(healthcheck_token_ns)
