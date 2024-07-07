"""
AdminPanel Service Class
"""

import datetime

from flask_admin_panel.interfaces import IAdminPanelService
from flask_admin_panel.exceptions.exceptions_classes import ModelNotFoundException
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DateTimeField,
    FloatField,
    IntegerField,
    StringField,
)
from injector import inject
from wtforms.validators import DataRequired, Optional
from wtforms_alchemy import ModelForm, model_form_factory
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class AdminPanelService(IAdminPanelService):
    """
    Service Class for AdminPanel
    """

    @inject
    def __init__(self, app: Flask, db: SQLAlchemy) -> None:
        """
        init method to set class variables
        """
        self.app = app
        self.db = db
        self.models_for_admin_panel: dict = {}
        self.app_title = "App Admin Panel"
        self.BaseModelForm = model_form_factory(FlaskForm)

    def registeration(self):
        pass

    def register_model_for_admin_panel(self, model_name: str, model_cls):
        """Register a model for admin panel"""
        self.models_for_admin_panel.update({model_name: model_cls})
        self.generate_model_config(model_name=model_name)

    def get_model_columnnames(self, model_class):
        """Get list of model column names"""
        return list(model_class.__table__.columns.keys())

    def get_model_properties(self, model_class):
        """Get list of model properites defined by user"""
        properties = []
        for prop in dir(model_class):
            if prop in ["query"]:
                continue
            if isinstance(getattr(model_class, prop, None), property):
                properties.append(prop)
        return properties

    def generate_model_form(self, model_class):
        """Generate model form"""

        class CustomModelForm(ModelForm):
            @classmethod
            def get_session(cls):
                return self.db.session

        # Get columns from SQLAlchemy model
        columns = self.get_model_columnnames(model_class)
        # Generate fields for recognized column types
        fields = {}
        for column in columns:
            field = None
            column_name = column
            column_info = model_class.__table__.columns[column]
            column_type = column_info.type.python_type
            validators = [DataRequired()] if not column_info.nullable else [Optional()]
            is_auto_incr_pk = column_info.autoincrement and column_info.primary_key
            if column_info.default is not None:
                validators.append(Optional())

            if is_auto_incr_pk:
                continue
            elif column_type in [str]:
                # Example: String fields
                field = StringField(column_name, validators=validators)
            elif column_type in [int]:
                # Example: Integer  fields
                field = IntegerField(column_name, validators=validators)
            elif column_type in [bytes, bool]:
                # Example: Boolean fields
                field = BooleanField(column_name, validators=validators)
            elif column_type in [float]:
                # Example: Float field
                field = FloatField(column_name, validators=validators)
            elif column_type in [datetime.date]:
                # Example: Date field
                field = DateField(column_name, validators=validators, format="%Y-%m-%d")
            elif column_type in [datetime.datetime]:
                # Example: DateTime field
                field = DateTimeField(
                    column_name, validators=validators, format="%Y-%m-%d %H:%M:%S"
                )
            else:
                # Skip unsupported column types or customize as needed
                continue
            if field:
                fields[column_name] = field
        # Dynamically create the form class
        form_class = type("DynamicModelForm", (CustomModelForm,), fields)
        return form_class

    def generate_model_config(self, model_name):
        """Generate forms dynamically for given model"""
        model_class = self.models_for_admin_panel[model_name]
        column_names = self.get_model_columnnames(model_class)
        properties = self.get_model_properties(model_class)
        form_class = self.generate_model_form(model_class)
        self.models_for_admin_panel[model_name] = {
            "model": model_class,
            "form": form_class,
            "columns": column_names,
            "properties": properties,
        }

    def regenerate_all_model_configs(self):
        """Generate forms dynamically for each model"""
        for model_name in self.models_for_admin_panel.keys():
            self.generate_model_config(model_name=model_name)

    def get_model_info(self, model_name):
        """get model object"""
        model = self.models_for_admin_panel.get(model_name)
        return model

    def list_records(self, model_name):
        """List all the records of the model"""
        model = self.get_model_info(model_name)
        if model:
            records = model["model"].query.all()
            columns = model["columns"] + model["properties"]
            return records, columns
        raise ModelNotFoundException(
            f"{model_name} not found in registered models for Admin Panel"
        )

    def get_a_records(self, model_cls, id):
        """Get a record by PK ID"""
        return model_cls.query.get(id)

    def add_record(self, request, model_name):
        """Add a record to the model"""
        model = self.get_model_info(model_name)
        if model:
            form = model["form"](request.form)
            if request.method == "POST" and form.validate():
                instance = model["model"]()
                form.populate_obj(instance)
                self.db.session.add(instance)
                self.db.session.commit()
                return True, model_name, form
            return False, model_name, form
        raise ModelNotFoundException(
            f"{model_name} not found in registered models for Admin Panel"
        )

    def edit_record(self, request, model_name, id):
        """Edit Existing Record from the model"""
        model = self.get_model_info(model_name)
        if model:
            instance = model["model"].query.get(id)
            form = model["form"](request.form, obj=instance)
            if request.method == "POST" and form.validate():
                form.populate_obj(instance)
                self.db.session.commit()
                return True, model_name, form
            return False, model_name, form
        raise ModelNotFoundException(
            f"{model_name} not found in registered models for Admin Panel"
        )

    def delete_record(self, request, model_name, id):
        """Delete the Records from the model"""
        model = self.get_model_info(model_name)
        if model:
            instance = model["model"].query.get(id)
            if instance:
                self.db.session.delete(instance)
                self.db.session.commit()
                return True, model_name, instance
            return False, model_name, instance
        raise ModelNotFoundException(
            f"{model_name} not found in registered models for Admin Panel"
        )
