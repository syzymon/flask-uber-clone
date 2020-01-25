# -*- coding: utf-8 -*-
"""Driver user models."""
from flask_uber_clone.user.models import User

from flask_uber_clone.database import (
    db,
    Model,
    Column,
    SurrogatePK,
    reference_col
)


class Car(SurrogatePK, Model):
    """A car used to drive passengers"""
    __tablename__ = "cars"

    places_count = Column(db.Integer, nullable=False)

    car_name = Column(db.VARCHAR(50), nullable=True)
    lic_plate = Column(db.VARCHAR(16), nullable=True)


class Driver(User):
    """An employee allowed to drive."""
    __mapper_args__ = {
        'concrete': True
    }

    __tablename__ = "drivers"

    rating = Column(db.Float(precision=10, asdecimal=True), nullable=False,
                    default=0)
    experience = Column(db.Integer, nullable=False, default=0)

    car_id = reference_col("cars", nullable=True)
