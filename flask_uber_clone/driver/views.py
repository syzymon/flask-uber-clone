# -*- coding: utf-8 -*-
"""Driver section, including drive selection and car management."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app)
from flask_login import login_required, login_user, logout_user, current_user
from flask_paginate import Pagination, get_page_parameter

from flask_uber_clone.rider.models import PendingOrder
from flask_uber_clone.utils import flash_errors
from .forms import DriverLoginForm, DriverRegisterForm, AcceptOrderForm, \
    FinishOrderForm
from .models import Driver, TakenOrder

blueprint = Blueprint("driver", __name__, static_folder="../static")


def load_user(user_id):
    """Load user by ID."""
    user_id = int(user_id)
    if user_id % 2 == 0:
        return None
    return Driver.get_by_id(user_id / 2)


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
@login_required
def home():
    if current_user.taken_order:
        finish_form = FinishOrderForm()
        return render_template("driver/taken_order.html",
                               finish_form=finish_form,
                               order=current_user.taken_order)

    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (page - 1) * per_page

    orders_query = PendingOrder.query
    orders = orders_query.limit(per_page).offset(offset)

    pagination = Pagination(page=page, per_page=per_page,
                            total=orders_query.count(),
                            search=search,
                            bs_version=4,
                            record_name='orders')

    return render_template("driver/index.html", orders=orders,
                           pagination=pagination)


@blueprint.route("/order/<int:order_id>", methods=["GET", "POST"])
@login_required
def order(order_id):
    pending = PendingOrder.query.get_or_404(order_id)
    form = AcceptOrderForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            TakenOrder.create_from_pending(pending, current_user.id)
            pending.delete()
            return redirect(url_for("driver.home"))

    return render_template("driver/order.html", order=pending, accept_form=form)


@blueprint.route("/order/<int:order_id>/finish", methods=["POST"])
@login_required
def finish_order(order_id):
    taken = TakenOrder.query.get_or_404(order_id)
    form = FinishOrderForm(request.form)

    if form.validate_on_submit():
        current_app.logger.info("Valid!")

    return redirect(url_for("driver.home"))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Driver login."""
    if current_user.is_authenticated:
        return redirect(url_for("driver.home"))
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
