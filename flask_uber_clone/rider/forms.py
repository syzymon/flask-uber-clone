# -*- coding: utf-8 -*-
"""Rider forms."""
from flask_uber_clone.user.forms import RegisterForm
from .models import Rider


class RiderRegisterForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = Rider.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = Rider.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False

        return True
