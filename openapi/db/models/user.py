#-*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import uuid
from logbook import Logger
import datetime
from openapi.utils.exception_handle import IsExist, DefalutError

log = Logger('db/user')

class User(db.Entity):
    _table_ = 'user'

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    username = Required(str)
    password = Required(str)
    info = Optional(str)


    @classmethod
    @db_session
    def register(cls, username, password):
        obj = get(n for n in User if n.username == username)
        if obj:
            raise IsExist(title='此用户已经存在', detail=f'用户名{username}已经存在', type='LoginError')
        else:
            User(username=username, password=password)


    @classmethod
    @db_session
    def login(cls, username, password):
        obj = get(n for n in User if n.username == username and n.password == password)
        if not obj:
            raise DefalutError(title=f'用户名密码不正确', detail=f'用户名密码不正确')
        return obj.uid


    @classmethod
    @db_session
    def user_is_valid(cls, username, uid):
        obj = get(n for n in User if n.username == username and n.uid == uid)
        if obj:
            return True
        else:
            raise DefalutError(title=f'token已失效', detail=f'token已失效', status=401, type='AuthError')
