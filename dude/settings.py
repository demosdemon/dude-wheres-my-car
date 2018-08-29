# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import json
from base64 import b64decode

from environs import Env

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
    platform_relationships = json.loads(b64decode(platform_relationships.decode('ascii')))
    SQLALCHEMY_DATABASE_URI = fmt.format_map(platform_relationships['postgres'])
    # TODO: redis
else:
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
BCRYPT_HANDLE_LONG_PASSWORDS = True
BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
CACHE_TYPE = 'redis'  # Can be "memcached", "redis", etc.
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'
