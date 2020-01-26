# -*- coding: utf-8 -*-
"""Rider user models."""
import datetime

from flask_uber_clone.database import (
    db,
    Model,
    Column,
    SurrogatePK,
    reference_col,
    relationship
)

from flask_uber_clone.user.models import User


class Rider(User):
    """A user eligible to order a ride."""
    __mapper_args__ = {
        'concrete': True
    }

    __tablename__ = "riders"

    def get_id(self):
        return 2 * self.id


class Route(SurrogatePK, Model):
    __tablename__ = "routes"

    x1 = Column(db.Integer, nullable=False)
    y1 = Column(db.Integer, nullable=False)
    x2 = Column(db.Integer, nullable=False)
    y2 = Column(db.Integer, nullable=False)


class Order(SurrogatePK, Model):
    __tablename__ = "orders"

    rider_id = reference_col("riders", nullable=False)
    route_id = reference_col("routes", nullable=False)

    people_count = Column(db.Integer, default=1)

    date = Column(db.DateTime, default=datetime.datetime.utcnow)

    route = relationship("Route", backref="order", cascade="delete")
