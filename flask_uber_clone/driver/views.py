# -*- coding: utf-8 -*-
"""Driver section, including drive selection and car management."""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_uber_clone.extensions import login_manager
from .models import Driver

blueprint = Blueprint("driver", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return Driver.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET"])
def home():
    return render_template("rider/index.html")
