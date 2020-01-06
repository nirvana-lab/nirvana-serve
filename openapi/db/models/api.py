#-*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import uuid
import datetime
from openapi.utils.exception_handle import IsExist, DefalutError, IsNotExist
from logbook import Logger
from openapi.db.models.project import Project

log = Logger('db/api')

class Api(db.Entity):
    _table_ = 'api'

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    api_info = Required(Json)
    user = Required(str)
    info = Optional(Json)
    path = Required(str)
    method = Required(str)
    project = Required(Project)

    @classmethod
    @db_session
    def create(cls, namespace_id, project_id, api_object, method, path, user):
        obj = get(n for n in Api if n.method == method and n.path == path and n.delete_at == None and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None)
        if obj:
            raise IsExist(title='存在path和method同名的Api', detail=f'已经存在，uid为{obj.uid}')
        Api(api_info=api_object, user=user, path=path, method=method, project=project_id)

    @classmethod
    @db_session
    def list(cls, namespace_id, project_id):
        print(namespace_id, project_id)
        objs = select(n for n in Api if n.delete_at == None and n.project.id == project_id and
                      n.project.delete_at == None and n.project.namespace.id == namespace_id and
                      n.project.namespace.delete_at == None)
        data = []
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'uid': obj.uid,
                'path': obj.path,
                'method': obj.method,
                # 'api': obj.api_info
            }
            data.append(tmp_dict)
        return data