# -*- coding: utf-8 -*-
"""Rider forms."""
from flask_wtf import FlaskForm

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
    pass
