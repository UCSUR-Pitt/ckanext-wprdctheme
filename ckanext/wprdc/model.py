import uuid

import ckan.model as model
from ckan.common import request

from sqlalchemy import types, Column, Table, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.sql import func

def make_uuid():
    return unicode(uuid.uuid4())

def get_ip():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', '')
    if not ip:
        ip = request.environ.get('REMOTE_ADDR','Unknown IP Address')
    return ip

metadata = MetaData()

user_agreement_table = Table('user_agreement', metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid()),
    Column('ip_addr', types.UnicodeText, nullable=False),
    Column('agreed_on', types.DateTime, server_default=func.current_timestamp()),
)

def init_tables():
    metadata.create_all(model.meta.engine)

class UserAgreement(object):

    def __init__(self, id='', ip_addr=None):
        self.id = make_uuid()
        self.ip_addr = get_ip()

    def insert_new_agreement(self):
        new = UserAgreement(
            ip_addr=get_ip()
        )
        model.Session.add(new)
        model.Session.commit()

mapper(UserAgreement, user_agreement_table)
