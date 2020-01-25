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

from flask_uber_clone.utils import flash_errors

from .models import Rider
from .forms import RiderRegisterForm

blueprint = Blueprint("rider", __name__, static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("rider/index.html")


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RiderRegisterForm(request.form)
    if form.validate_on_submit():
        Rider.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)
