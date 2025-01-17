# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template, globals, request

from flask_uber_clone import commands, public, rider, driver
from flask_uber_clone.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
    flask_seeder,
    flask_breadcrumbs
)


@login_manager.user_loader
def load_user(user_id):
    """
    This will be used many times like on using current_user
    :param user_id: username
    :return: user or none
    """
    # http://librelist.com/browser/flask/2012/4/7/current-blueprint/#44814417e8289f5f5bb9683d416ee1ee
    if not request.endpoint:
        return None

    blueprint = globals.current_app.blueprints[request.blueprint]

    if hasattr(blueprint, "load_user"):
        return blueprint.load_user(user_id)

    # https://flask-login.readthedocs.org/en/latest/#how-it-works
    return None


def create_app(config_object="flask_uber_clone.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    flask_seeder.init_app(app, db)
    flask_breadcrumbs.init_app(app, init_menu=False)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(rider.views.blueprint, url_prefix="/ride")
    app.register_blueprint(driver.views.blueprint, url_prefix="/drive")
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
