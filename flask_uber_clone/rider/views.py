# -*- coding: utf-8 -*-
"""Customer section, including customer registration and ride requesting."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

blueprint = Blueprint("rider", __name__, static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("rider/index.html")
