from .devConfig import DevConfig
from .prodConfig import ProdConfig
from .testConfig import TestConfig
from .db_schema import DB_SCHEMA
from .app_constants import API_SECRET_KEY
config_by_name = {
    "development":DevConfig,
    "testing":TestConfig,
    "production":ProdConfig
}