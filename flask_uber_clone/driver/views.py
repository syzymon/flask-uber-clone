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
from flask_login import login_required, login_user, logout_user

from flask_uber_clone.utils import flash_errors
from .models import Driver
from .forms import DriverLoginForm, DriverRegisterForm

blueprint = Blueprint("driver", __name__, static_folder="../static")


def load_user(user_id):
    """Load user by ID."""
    if user_id % 2 == 0:
        return None
    return Driver.get_by_id(int(user_id / 2))


@blueprint.record_once
def on_load(state):
    """
    http://stackoverflow.com/a/20172064/742173

    :param state: state
    """
    blueprint.load_user = load_user
    state.app.login_manager.blueprint_login_views[
        blueprint.name] = 'driver.login'


@blueprint.route("/", methods=["GET"])
def home():
    form = DriverLoginForm()
    return render_template("driver/index.html", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Driver login."""
    form = DriverLoginForm(request.form)
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for(
                "driver.home")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/login.html", form=form)


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = DriverRegisterForm(request.form)
    if form.validate_on_submit():
        Driver.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("driver.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(request.args.get("next") or url_for("driver.home"))