# -*- coding: utf-8 -*-
"""Rider forms."""
from flask_wtf import FlaskForm

from flask_uber_clone.user.forms import LoginForm, RegisterForm
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, NumberRange
from .models import Rider


class RiderRegisterForm(RegisterForm):
    """Rider register form."""
    USER_MODEL = Rider


class RiderLoginForm(LoginForm):
    """Rider login form."""
    USER_MODEL = Rider


class NewOrderForm(FlaskForm):
    x1 = IntegerField("Pickup x", validators=[DataRequired()])
    y1 = IntegerField("Pickup y", validators=[DataRequired()])
    x2 = IntegerField("Destination x", validators=[DataRequired()])
    y2 = IntegerField("Destination y", validators=[DataRequired()])
    ppl_cnt = IntegerField("People count",
                           validators=[NumberRange(min=1, max=9)])

    def validate(self):
        initial_validation = super().validate()
        if not initial_validation:
            return False
        return True


class CancelOrderForm(FlaskForm):
    pass
