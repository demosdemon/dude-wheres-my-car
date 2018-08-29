# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from dude import commands, public, user
from dude.extensions import admin, alembic, bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager


def create_app(config_object='dude.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0], instance_relative_config=True)
    app.config.from_object(config_object)
    app.config.from_envvar('DUDE_SETTINGS', silent=True)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    admin.init_app(app)
    alembic.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

# import os

# from flask import Flask
# from flask_bcrypt import Bcrypt

# from . import admin, config, db

# bcrypt = Bcrypt()


# def create_app(test_config=None):
#     app = Flask(__name__.split('.')[0], instance_relative_config=True)
#     config.init_app(app, test_config)

#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     bcrypt.init_app(app)
#     db.init_app(app)
#     admin.init_app(app)

#     config.validate(app)
#     return app