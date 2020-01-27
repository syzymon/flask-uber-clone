# -*- coding: utf-8 -*-
"""Rider forms."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length

from flask_uber_clone.user.forms import LoginForm, RegisterForm
from .models import Driver


class DriverRegisterForm(RegisterForm):
    """Rider register form."""
    USER_MODEL = Driver

    first_name = StringField(label="First name (optional)",
                             validators=[Length(max=30)])

    last_name = StringField(label="Last name (optional)",
                            validators=[Length(max=30)])


class DriverLoginForm(LoginForm):
    """Rider login form."""
    USER_MODEL = Driver


class AcceptOrderForm(FlaskForm):
    pass


class FinishOrderForm(FlaskForm):
    fare_rate = DecimalField(label="Enter fare rate when ride finished",
                             places=2,
                             validators=[DataRequired(), NumberRange(0, 5)])


class LocationForm(FlaskForm):
    x = IntegerField(label="X",
                     validators=[DataRequired(), NumberRange(-100, 100)])
    y = IntegerField(label="Y",
                     validators=[DataRequired(), NumberRange(-100, 100)])


class CarForm(FlaskForm):
    car_name = StringField(label="Car name",
                           validators=[Length(max=25)])

    lic_plate = StringField(label="License plates",
                            validators=[DataRequired(), Length(min=1, max=16)])

    places_count = IntegerField(label="Places count",
                                validators=[DataRequired(), NumberRange(1, 9)])


class SelectCarForm(FlaskForm):
    car_id = IntegerField(label="Car id", validators=[DataRequired()])
