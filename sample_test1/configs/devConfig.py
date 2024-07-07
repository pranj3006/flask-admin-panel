import os

from .baseConfig import BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))

class DevConfig(BaseConfig):
    DEBUG = True