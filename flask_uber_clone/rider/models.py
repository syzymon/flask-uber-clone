# -*- coding: utf-8 -*-
"""Rider user models."""
import datetime

from sqlalchemy.ext.declarative.base import declared_attr

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
    __tablename__ = "riders"

    def get_id(self):
        return 2 * self.id

    __mapper_args__ = {
        "concrete": True
    }


class Route(SurrogatePK, Model):
    __tablename__ = "routes"

    x1 = Column(db.Integer, nullable=False)
    y1 = Column(db.Integer, nullable=False)
    x2 = Column(db.Integer, nullable=False)
    y2 = Column(db.Integer, nullable=False)


class OrderState(SurrogatePK, Model):
    """Abstract class representing order state (an integral part of order
    executions which consists of several steps like issuing, taking, finishing
    the order."""
    __abstract__ = True

    @declared_attr
    def rider_id(cls):
        return reference_col("riders", nullable=False)

    @declared_attr
    def route_id(cls):
        return reference_col("routes", nullable=False)

    people_count = Column(db.Integer, default=1)

    issued = Column(db.DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def route(cls):
        return relationship("Route")


class PendingOrder(OrderState):
    __tablename__ = "orders"

    rider = relationship("Rider",
                         backref=db.backref("pending_order", uselist=False))

    __mapper_args__ = {
        "polymorphic_identity": "orders",
        "concrete": True
    }
