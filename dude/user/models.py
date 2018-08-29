# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

from dude.database import Column, Model, SurrogatePK, db, reference_col, relationship
from dude.extensions import admin, bcrypt

now = dt.datetime.utcnow


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.Unicode(128), unique=True, nullable=False)
    email = Column(db.String(255), unique=False, nullable=False, index=True)
    email_verified = Column(db.Boolean, nullable=False, default=False)
    created_at = Column(db.DateTime, nullable=False, default=now)
    modified_at = Column(db.DateTime, nullable=False, default=now, onupdate=now)

    # the hashed password
    password = Column(db.Binary(128), nullable=True)
    password_set_at = Column(db.DateTime, nullable=True)
    # used to expire the reset token
    password_reset_at = Column(db.DateTime, nullable=True)
    # used to validate the reset request
    password_reset_token = Column(db.Binary(128), nullable=True)

    first_name = Column(db.Unicode(50), nullable=True)
    last_name = Column(db.Unicode(50), nullable=True)
    is_active = Column(db.Boolean, nullable=False, default=False)
    is_admin = Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)
        self.password_set_at = now()

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
