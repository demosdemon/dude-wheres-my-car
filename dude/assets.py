"""App asset manager."""
import os


class Assets(object):
    """Asset manager flask extension."""

    def __init__(self, app=None):
        """Initialize the extension."""
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Mutate the application passed according to http://flask.pocoo.org/docs/1.0/extensiondev/.

        Installs template functions.
        """
        app.config.setdefault('STATIC_MANIFEST_PATH', 'static/manifest.json')
        app.config.setdefault('STATIC_FILES', 'static/')
        app.config.setdefault('STATIC_URL', '/static')
