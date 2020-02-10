# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from logbook import Logger
from openapi.db.models.namespace import Namespace
from openapi.utils.exception_handle import IsExist, IsNotExist
import uuid

log = Logger('db/env')

class Env(db.Entity):
    _table_ = 'env'

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    env = Required(str)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime,  nullable=True)
    user = Required(str)
    url = Required(str)
    description = Optional(str, nullable=True)
    info = Optional(Json)
    namespace = Required(Namespace)

    @classmethod
    @db_session
    def create(cls, namespace_id, env, url, description, user):
        obj = get(n for n in Env if n.env == env and n.delete_at == None and
                  n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            raise IsExist(title='不能创建同名的环境', detail=f'{env}已经存在, uuid为{obj.uid}')
        else:
            obj = Env(env=env, description=description, user=user, namespace=namespace_id, url=url)
            return obj


    @classmethod
    @db_session
    def list(cls, namespace_id):
        objs = select(n for n in Env if n.namespace.id == namespace_id and n.namespace.delete_at == None
                      and n.delete_at == None).order_by(Env.id)
        data = []
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'name': obj.env,
                'url': obj.url,
                'description': obj.description
            }
            data.append(tmp_dict)
        return data


    @classmethod
    @db_session
    def update(cls, namespace_id, env_id, env, url, description, user):
        obj = get(n for n in Env if n.env == env and n.delete_at == None and
                  n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            raise IsExist(title='修改的环境名已经存在', detail=f'{env}已经存在, uuid为{obj.uid}')

        obj = get(n for n in Env if n.id == env_id and n.delete_at == None and
                  n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            obj.env = env
            obj.url = url
            obj.description = description
            obj.update_at = datetime.datetime.utcnow()
            obj.user = user
        else:
            raise IsNotExist(title='修改的环境不存在', detail=f'id为{env_id}的环境不存在')

    @classmethod
    @db_session
    def delete(cls, namespace_id, env_id, user):
        obj = get(n for n in Env if n.id == env_id and n.delete_at == None and
                  n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            obj.delete_at = datetime.datetime.utcnow()
            obj.user = user
        else:
            raise IsNotExist(title='删除的环境不存在', detail=f'id为{env_id}的环境不存在')