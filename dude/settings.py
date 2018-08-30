# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

import dude.platform

env = Env()
env.read_env()

plat = dude.platform.environment

if plat.project_entropy:
    SECRET_KEY = plat.project_entropy
else:
    SECRET_KEY = env.str('SECRET_KEY')

if plat.relationships:
    SQLALCHEMY_DATABASE_URI = next(plat.get_service_urls('postgres'))
    CACHE_REDIS_URL = next(plat.get_service_urls('redis'))
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
