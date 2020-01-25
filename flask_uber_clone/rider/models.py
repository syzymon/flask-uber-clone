# -*- coding: utf-8 -*-
"""Rider user models."""
from flask_uber_clone.user.models import User


class Rider(User):
    """A user eligible to order a ride."""
    __mapper_args__ = {
        'concrete': True
    }

    def get_id(self):
        return 2 * self.id

    __tablename__ = "riders"
