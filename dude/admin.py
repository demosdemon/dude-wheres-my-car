"""Admin config."""
from flask_admin.contrib.sqla import ModelView

from dude.extensions import admin, db
from dude.user.models import Role, User

admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
