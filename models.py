"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table('pantry',
    Field('userID', 'reference auth_user'),
    Field('item', requires=IS_NOT_EMPTY()),
    # Field('quantity', 'float', requires=IS_FLOAT_IN_RANGE(0, 1e6)),
)

db.commit()
