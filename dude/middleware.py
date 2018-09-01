"""Dude Middleware."""


class ClacksOverhead(object):
    """Inject HTTP headers into your response."""

    def __init__(self, app=None, *headers, **kwargs):
        """Initialize the header injector."""
        self.headers = (headers or (
            ('X-Clacks-Overhead', 'GNU'),
        )) + tuple(kwargs.items())
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the application."""
        app.after_request(self)

    def __call__(self, response):
        """Handle our part of the request."""
        response.headers.extend(self.headers)
        return response
