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

    @classmethod
    @db_session
    def get_detail_by_id(cls, namespace_id, project_id, api_id):
        obj = get(n for n in Api if n.delete_at == None and n.id == api_id and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None)
        if obj:
            return {
                'id': obj.id,
                'uid': obj.uid,
                'path': obj.path,
                'method': obj.method,
                'api_info': obj.api_info
            }
        else:
            raise IsNotExist(title='Api不存在', detail=f'id为{api_id}的接口不存在')

    @classmethod
    @db_session
    def update_api_by_id(cls, namespace_id, project_id, api_id, api_obj, path, method, user):
        obj = get(n for n in Api if n.delete_at == None and n.id == api_id and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None and
                  n.path == path and n.method == method)
        if obj:
            obj.api_info = api_obj
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='Api不存在', detail=f'id为{api_id}的接口不存在')