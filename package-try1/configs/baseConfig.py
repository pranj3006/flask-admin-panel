import os
from datetime import timedelta
from urllib.parse import quote

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY",os.urandom(24))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY",os.urandom(24))

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    host = os.getenv("MSSQL_SERVER","") + ":" + os.getenv("MSSQL_PORT","")
    username = os.getenv("MSSQL_USERNAME","")
    password = os.getenv("MSSQL_PASSWORD","")
    database = os.getenv("MSSQL_DATABASE","")

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{username}:{quote(password)}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    JWT_SECRET_KEY = b'X19\xf8Gh]\xe1\xab\n\xc5+`\xdfe\x8d\xa6$y\xbe\xc0|\xc4-'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,
        "max_overflow": 5,
        "pool_timeout": 30,
        "pool_recycle": 3600,

    }

    