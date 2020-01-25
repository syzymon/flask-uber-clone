# -*- coding: utf-8 -*-
"""Rider user models."""
from flask_uber_clone.user.models import User


class Rider(User):
    """An user eligible to order a ride."""
    __mapper_args__ = {
        'concrete': True
    }

    __tablename__ = "riders"
