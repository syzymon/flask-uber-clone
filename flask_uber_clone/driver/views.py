# -*- coding: utf-8 -*-
"""Driver section, including drive selection and car management."""
import math

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import login_required, login_user, logout_user, current_user
from flask_paginate import Pagination, get_page_parameter

from flask_uber_clone.rider.models import Route, PendingOrder
from flask_uber_clone.utils import flash_errors
from .forms import DriverLoginForm, DriverRegisterForm, AcceptOrderForm, \
    FinishOrderForm, LocationForm, CarForm, SelectCarForm
from .models import Driver, TakenOrder, FinishedOrder, Car

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


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def home():
    if current_user.taken_order:
        finish_form = FinishOrderForm()
        finish_form.fare_rate.data = 2.137
        return render_template("driver/taken_order.html",
                               finish_form=finish_form,
                               order=current_user.taken_order)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (page - 1) * per_page

    location_form = LocationForm(request.form)

    orders_query = PendingOrder.query.join(Route)
    orders_sorted = orders_query.order_by(Route.length.desc())

    coords = (0, 0)

    if request.method == "POST":
        if location_form.validate_on_submit():
            orders_sorted = orders_query.order_by(Route.distance(
                x=location_form.x.data,
                y=location_form.y.data
            ))

            coords = (location_form.x.data,
                      location_form.y.data)
        else:
            flash_errors(location_form)

    orders = orders_sorted.limit(per_page).offset(offset)

    pagination = Pagination(page=page, per_page=per_page,
                            total=orders_sorted.count(),
                            bs_version=4,
                            record_name='orders')

    return render_template("driver/index.html", orders=orders,
                           location_form=location_form,
                           coords=coords,
                           pagination=pagination)


@blueprint.route("/order/<int:order_id>", methods=["GET", "POST"])
@login_required
def order(order_id):
    if current_user.taken_order:
        return redirect(url_for("driver.home"))

    pending = PendingOrder.query.get_or_404(order_id)
    form = AcceptOrderForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            TakenOrder.create_from_pending(pending, current_user.id)
            pending.delete()
            return redirect(url_for("driver.home"))

    return render_template("driver/order.html", order=pending,
                           accept_form=form)


@blueprint.route("/order/<int:order_id>/finish", methods=["POST"])
@login_required
def finish_order(order_id):
    taken = TakenOrder.query.get_or_404(order_id)
    form = FinishOrderForm(request.form)

    if form.validate_on_submit():
        finished = FinishedOrder.create_from_taken(taken)

        calculated_price = taken.route.length * float(
            form.fare_rate.data) * math.log1p(taken.people_count)

        finished.update(price=round(calculated_price, 2))
        taken.delete()
    else:
        flash_errors(form)

    return redirect(url_for("driver.home"))


@blueprint.route("/history", methods=["GET"])
@login_required
def history():
    return render_template("driver/history.html")


@blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("driver/profile.html")


@blueprint.route("/vehicles", methods=["GET"])
@login_required
def vehicles():
    return render_template("driver/vehicles.html")


@blueprint.route("/vehicles/add", methods=["GET", "POST"])
@login_required
def add_vehicle():
    car_form = CarForm(request.form)

    if request.method == "POST":
        if car_form.validate_on_submit():
            car = Car()
            car_form.populate_obj(car)
            car.owner_id = current_user.id
            car.save()

            return redirect(url_for("driver.vehicle", vehicle_id=car.id))
        else:
            flash_errors(car_form)

    return render_template("driver/new_vehicle.html", car_form=car_form)


@blueprint.route("/vehicle/<int:vehicle_id>", methods=["GET"])
@login_required
def vehicle(vehicle_id):
    car = Car.query.get_or_404(vehicle_id)

    select_form = SelectCarForm()
    select_form.car_id.data = car.id

    return render_template("driver/vehicle.html", vehicle=car,
                           select_form=select_form)


@blueprint.route("/vehicle/<int:vehicle_id>/select", methods=["POST"])
@login_required
def select_vehicle(vehicle_id):
    current_user.update(current_car_id=vehicle_id)
    return redirect(url_for("driver.vehicles"))


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
