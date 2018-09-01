"""Dude Middleware."""


class ClacksOverhead(object):
    """Inject HTTP headers into your response."""

    def __init__(self, app, *headers, **kwargs):
        """Initialize the header injector."""
        self.app = app
        self.headers = (headers or (
            ('X-Clacks-Overhead', 'GNU'),
        )) + tuple(kwargs.items())

        self.__start_response = None

    def __call__(self, environ, start_response):
        """Handle our part of the request."""
        self.__start_response = start_response
        return self.app(environ, self.start_response)

    def start_response(self, status, headers, exc_info=None):
        """Handle our part of the response."""
        headers.extend(self.headers)
        return self.__start_response(status, headers, exc_info)
