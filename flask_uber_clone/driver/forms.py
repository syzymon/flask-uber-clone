# -*- coding: utf-8 -*-
"""Rider forms."""
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DecimalField
from wtforms.validators import DataRequired, NumberRange

from flask_uber_clone.user.forms import LoginForm, RegisterForm
from .models import Driver


class DriverRegisterForm(RegisterForm):
    """Rider register form."""
    USER_MODEL = Driver


class DriverLoginForm(LoginForm):
    """Rider login form."""
    USER_MODEL = Driver


class AcceptOrderForm(FlaskForm):
    pass


class FinishOrderForm(FlaskForm):
    fare_rate = DecimalField(label="Enter fare rate when ride finished",
                             places=2,
                             validators=[DataRequired(), NumberRange(0, 5)])
