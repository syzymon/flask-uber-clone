# -*- coding: utf-8 -*-
"""Driver user models."""
import datetime

from flask_uber_clone.database import (
    db,
    Model,
    Column,
    SurrogatePK,
    reference_col,
    relationship
)
from flask_uber_clone.rider.models import OrderState, PendingOrder
from flask_uber_clone.user.models import User


class Car(SurrogatePK, Model):
    """A car used to drive passengers"""
    __tablename__ = "cars"

    places_count = Column(db.Integer, nullable=False)

    car_name = Column(db.VARCHAR(50), nullable=True)
    lic_plate = Column(db.VARCHAR(16), nullable=True)

    current_driver_id = reference_col("drivers", nullable=True)
    driver = relationship("Driver", backref="cars")


class Driver(User):
    """An employee allowed to drive."""
    __tablename__ = "drivers"

    rating = Column(db.Float(precision=10, asdecimal=True), nullable=False,
                    default=0)
    experience = Column(db.Integer, nullable=False, default=0)

    def get_id(self):
        return 2 * self.id + 1

    __mapper_args__ = {
        "concrete": True
    }


class TakenOrder(OrderState):
    __tablename__ = "jobs"

    driver_id = reference_col("drivers")
    driver = relationship("Driver",
                          backref=db.backref("taken_order", uselist=False))

    taken = Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def create_from_pending(cls, pending: PendingOrder, driver_id: int):
        return cls.create(
            rider_id=pending.rider_id,
            route_id=pending.route_id,
            people_count=pending.people_count,
            issued=pending.issued,
            driver_id=driver_id
        )

    __mapper_args__ = {
        "polymorphic_identity": "jobs",
        "concrete": True
    }


class FinishedOrder(OrderState):
    __tablename__ = "finished"

    driver_id = reference_col("drivers")
    driver = relationship("Driver",
                          backref=db.backref("finished_orders"))

    price = Column(db.Float, nullable=True)
    rating = Column(db.Float, nullable=True)

    taken = Column(db.DateTime)
    finished = Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def create_from_taken(cls, taken_order: TakenOrder):
        return cls.create(
            rider_id=taken_order.rider_id,
            route_id=taken_order.route_id,
            people_count=taken_order.people_count,
            issued=taken_order.issued,
            driver_id=taken_order.driver_id,
            taken=taken_order.taken
        )

    __mapper_args__ = {
        "polymorphic_identity": "finished",
        "concrete": True
    }
