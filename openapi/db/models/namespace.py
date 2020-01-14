# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import uuid
import datetime
from openapi.utils.exception_handle import IsExist, IsNotExist
from logbook import Logger

log = Logger('db/namespace')

class Namespace(db.Entity):

    _table_ = 'namespace'
    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    namespace = Required(str)
    description = Optional(str, nullable=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime,  nullable=True)
    user = Required(str)
    info = Optional(Json)
    project = Set('Project')

    @classmethod
    @db_session
    def create(cls,namespace, description, user):
        obj = get(n for n in Namespace if n.namespace == namespace and n.delete_at == None)
        if obj:
            raise IsExist(title='不能创建同名的namespace', detail=f'{namespace}已经存在, uuid为{obj.uid}')
        Namespace(namespace=namespace, description=description, user=user)

    @classmethod
    @db_session
    def list(cls):
        objs = select(n for n in Namespace if n.delete_at == None).order_by(Namespace.id)
        data = []
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                # 'uid': obj.uid,
                'name': obj.namespace,
                'description': obj.description
            }
            data.append(tmp_dict)
        return data


    @classmethod
    @db_session
    def delete_namespace_by_id(cls, namespace_id, user):
        obj = get(n for n in Namespace if n.delete_at == None and n.id == namespace_id)
        if obj:
            obj.delete_at = datetime.datetime.utcnow()
            obj.user = user
        else:
            raise IsNotExist(title='Namespace不存在', detail=f'id为{namespace_id}的接口不存在')