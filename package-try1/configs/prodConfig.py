import os

from .baseConfig import BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))

class ProdConfig(BaseConfig):
    DEBUG = False