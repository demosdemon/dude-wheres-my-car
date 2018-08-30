# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import json
from base64 import b64decode

from environs import Env
from six.moves.urllib_parse import urlencode, urlunsplit


def make_netloc(data):
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
    scheme = data.get('scheme')
    netloc = make_netloc(data)
    path = data.get('path')
    query = data.get('query', {})
    query = urlencode(query)
    fragment = data.get('fragment')
    comps = (scheme, netloc, path, query, fragment)
    comps = map(lambda s: s or '', comps)
    return urlunsplit(comps)


env = Env()
env.read_env()
fmt = '{scheme}://{username}:{password}@{host}:{port}/{path}'

platform_project_entropy = env.str('PLATFORM_PROJECT_ENTROPY', default='')
platform_relationships = env.str('PLATFORM_RELATIONSHIPS', default='')

if platform_project_entropy:
    SECRET_KEY = platform_project_entropy
else:
    SECRET_KEY = env.str('SECRET_KEY')

if platform_relationships:
    platform_relationships = json.loads(b64decode(platform_relationships.encode('ascii')))
    postgres = platform_relationships['postgres'][0]
    redis = platform_relationships['redis'][0]
    SQLALCHEMY_DATABASE_URI = make_url(postgres)
    CACHE_REDIS_URL = make_url(redis)
else:
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
    CACHE_REDIS_URL = env.str('CACHE_REDIS_URL')

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'

BCRYPT_HANDLE_LONG_PASSWORDS = True
BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
CACHE_TYPE = 'redis'  # Can be "memcached", "redis", etc.
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'
