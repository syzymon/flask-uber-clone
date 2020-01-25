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
from flask_login import login_user, login_required, current_user

from flask_uber_clone.utils import flash_errors
from flask_uber_clone.extensions import login_manager

from .models import Rider
from .forms import RiderLoginForm, RiderRegisterForm

blueprint = Blueprint("rider", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return Rider.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("rider.register"))

    return render_template("rider/index.html")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Rider login."""
    form = RiderLoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for(
                "public.home")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return redirect(url_for("rider.home"))


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
