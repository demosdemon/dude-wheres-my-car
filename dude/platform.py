"""A module to process the Platform.sh environment."""

import base64
import json
import os
import shlex
from functools import partial
from itertools import chain, tee

from six.moves.urllib_parse import urlencode, urlunsplit

_json_vars = (
    'PLATFORM_APPLICATION',
    'PLATFORM_VARIABLES',
    'PLATFORM_RELATIONSHIPS',
    'PLATFORM_ROUTES',
)

_known_attrs = (
    'application',
    'application_name',
    'app_command',
    'branch',
    'dir',
    'environment',
    'project',
    'project_entropy',
    'relationships',
    'routes',
    'smtp_host',
    'tree_id',
    'variables',
)


def decode_json(data):
    """Decode a base64 encoded json string."""
    data = os.fsencode(data)
    data = base64.b64decode(data)
    return json.loads(data, object_pairs_hook=attrdict)


def make_name(key):
    """Return a string suitable for use as a python identifer from an environment key."""
    return key.replace('PLATFORM_', '').lower()


def make_netloc(data):
    """Make the `netloc` portion of a url from a `dict` of values.

    If `netloc` is found in the `dict`, it is returned; otherwise, the `netloc`
    is `[{username}[:{password}]@]{hostname}[:{port}]`. If `hostname` is not
    found, `host` is used instead.

    If neither `netloc`, `hostname`, nor `host` are found, a `ValueError` is
    raised.
    """
    netloc = data.get('netloc')
    if netloc:
        return netloc

    username = data.get('username')
    password = data.get('password')
    hostname = data.get('hostname') or data.get('host')
    port = data.get('port')

    if not hostname:
        raise ValueError('requires at least one of netloc, hostname, or host')

    if username and password:
        username = '{}:{}'.format(username, password)

    netloc = '{}{}{}{}{}'.format(
        username or '',
        '@' if username else '',
        hostname,
        ':' if port else '',
        port or ''
    )


def make_url(data):
    """Construct a URL from a `dict` of components.

    Uses `scheme`, `netloc`, `username`, `password`, `hostname`, `host`,
    `port` (see `make_netloc`), `path`, `query`, and `fragment`.
    """
    scheme = data.get('scheme')
    netloc = make_netloc(data)
    path = data.get('path')
    query = data.get('query', {})
    query = urlencode(query)
    fragment = data.get('fragment')
    comps = (scheme, netloc, path, query, fragment)
    comps = map(lambda s: s or '', comps)
    return urlunsplit(comps)


class attrdict(dict):  # noqa: N801 # PascalCase warning
    """A `dict` that exposes its keys as attributes."""

    __slots__ = ()

    def __getattr__(self, name):
        """Return the key if it exists otherwise raise an AttributeError."""
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __dir__(self):
        """Return the dir() listing for this object.

        Includes the `dict` keys as they are exposed as attributes.
        """
        return chain(super(attrdict, self).__dir__(), self)


class EnvDescriptor(object):
    """A Member Descriptor to fetch an environment variable."""

    def __init__(self, variable, convert=None):
        """Initialize the descriptor with a variable name and converter function.

        The default `convert` function decodes the byte string from the operating
        system into a str.
        """
        self.variable = os.fsencode(variable)
        self.convert = convert or os.fsdecode

    def __get__(self, inst, owner=None):
        """Get the `self.variable` from the environment and apply the converter."""
        rv = os.getenvb(self.variable)
        if rv:
            return self.convert(rv)


class Environment(object):
    """A mixin class for the environment returned from `build_environment`."""

    __slots__ = ('_keys')

    def __init__(self, keys):
        """Initialize the environment object.

        The environment is provided with a list of its keys at initialization to
        speed up other string formatting functions.
        """
        self._keys = keys

    def __getattr__(self, name):
        """Do not raise an AttributeError if the `name` is in our list of known attrs."""
        if name in _known_attrs:
            return None

        raise AttributeError

    def __dir__(self):
        """Return the known attributes of this instance."""
        names = set(super(Environment, self).__dir__())
        names.update(_known_attrs)
        return names

    def __repr__(self):
        """Represent the environment in a human friendly way for debugging."""
        return '{}({})'.format(self.__class__.__name__, ', '.join(self._keys))

    def __str__(self):
        """Format the environment as a `.sh` file."""
        def quote(obj):
            if not isinstance(obj, str):
                obj = json.dumps(obj, sort_keys=True, separators=(',', ':'))
                obj = obj.encode('ascii')
                obj = base64.b64encode(obj)
                obj = obj.decode('ascii')

            return shlex.quote(obj)

        keys, values = tee(self._keys)
        values = map(make_name, values)
        values = map(partial(getattr, self), values)
        values = map(quote, values)
        items = map('declare -x {}={};\n'.format, keys, values)
        return ''.join(items)

    def get_relationship(self, name):
        """Return the raw list of relationships for `name`."""
        if self.relationships:
            return self.relationships[name]

    def get_service(self, service):
        """Return an iterator of relationships of type `service`."""
        if self.relationships:
            for value in self.relationships.values():
                for svc in value:
                    if svc.service == service:
                        yield svc

    def get_relationship_urls(self, name):
        """Return an iterator of urls to the relationship named `name`."""
        return map(make_url, self.get_relationship(name) or ())

    def get_service_urls(self, service):
        """Return an iterator of urls to the service of type `service`."""
        return map(make_url, self.get_service(service))


def build_environment(*extra_keys, **kwargs):
    """Build an object with the Platform.sh environment variables as properties.

    The function accepts extra environment variables as positional parameters.
    The function also decodes base64-json encoded variables provided as keyword
    arguments. JSON objects are decoded into `attrdict` objects.

    Example:

        >>> import os
        >>> import base64
        >>> import json
        >>> from dude.platform import build_environment
        >>> os.environ['SENDGRID_TOKEN'] = 'test'
        >>> os.environb[b'METADATA'] = base64.b64encode(os.fsencode(json.dumps({'test': True})))
        >>> environment = build_environment('SENDGRID_TOKEN', METADATA=True)
        >>> environment.application_name
        'dude'
        >>> environment.sendgrid_token
        'test'
        >>> environment.metadata
        {'test': True}
        >>> environment.metadata.test
        True
    """
    keys = [
        key
        for key in os.environ.keys()
        if key.startswith('PLATFORM')
        or key in extra_keys
        or key in kwargs
    ]

    is_json = set(_json_vars)
    is_json.update(kwargs)

    props = {
        make_name(key):
        EnvDescriptor(key, decode_json if key in is_json else None)
        for key in keys
    }

    klass = type(
        'PlatformEnvironment',
        (Environment, object, ),
        props
    )

    return klass(keys)


environment = build_environment()
