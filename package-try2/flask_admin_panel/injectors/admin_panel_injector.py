# """
# AdminPanel Injector Class definition
# """

from flask_admin_panel.services import AdminPanelService
from injector import Binder,  Module, singleton, Injector, provider
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# class AdminPanelModule(Module):
#     """
#     AdminPanel Injector Class definition
#     """    
#     def __init__(self, db: SQLAlchemy):
#         self.db = db

#     def configure(self, binder: Binder) -> None:
#         binder.bind(
#             SQLAlchemy, 
#             to=self.db, 
#             scope=singleton)
#         binder.bind(
#             AdminPanelService, 
#             to=AdminPanelService, 
#             scope=singleton)


class AdminPanelModule(Module):
    """
    AdminPanel Injector Class definition
    """    
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

    def configure(self, binder: Binder) -> None:
        binder.bind(
            Flask,
            to=self.app,
            scope=singleton)

        binder.bind(
            SQLAlchemy,
            to=self.db,
            scope=singleton)

        binder.bind(
            AdminPanelService,
            to=AdminPanelService,
            scope=singleton)



