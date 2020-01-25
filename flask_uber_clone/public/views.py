# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from flask_uber_clone.rider.forms import RiderLoginForm
from flask_uber_clone.rider.models import Rider
from flask_uber_clone.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = RiderLoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/login", methods=["GET"])
def dispatch_login():
    """Login dispatch between rider and driver"""
    return render_template("public/login_dispatch.html")


@blueprint.route("/register", methods=["GET"])
def dispatch_register():
    """Login dispatch between rider and driver"""
    return render_template("public/register_dispatch.html")


@blueprint.route("/about/")
def about():
    """About page."""
    form = RiderLoginForm(request.form)
    return render_template("public/about.html", form=form)
