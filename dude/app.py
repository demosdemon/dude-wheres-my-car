# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from dude import commands, public, user
from dude.extensions import admin, alembic, bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager
from dude.middleware import ClacksOverhead


def create_app(config_object='dude.settings'):
    """Return an application, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0], instance_relative_config=True)
    app.config.from_object(config_object)
    app.config.from_envvar('DUDE_SETTINGS', silent=True)
    register_middleware(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_context_processors(app)
    return app


def register_middleware(app):
    """Register Werkzeug middleware."""
    app.wsgi_app = ClacksOverhead(app.wsgi_app)


def register_extensions(app):
    """Register Flask extensions."""
    import dude.admin  # noqa
    admin.init_app(app)
    alembic.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


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


def register_context_processors(app):
    """Register the Jina2 Context Processors."""


def static_path(path):
    """Return a url to a static file in `/static`."""
