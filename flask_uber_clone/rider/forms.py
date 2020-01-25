# -*- coding: utf-8 -*-
"""Rider forms."""
from flask_wtf import FlaskForm

from flask_uber_clone.user.forms import LoginForm, RegisterForm
from .models import Rider


class RiderRegisterForm(RegisterForm):
    """Rider register form."""
    USER_MODEL = Rider


class RiderLoginForm(LoginForm):
    """Rider login form."""
    USER_MODEL = Rider
