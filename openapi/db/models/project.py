# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import uuid
import datetime
from openapi.utils.exception_handle import IsExist, DefalutError, IsNotExist
from logbook import Logger
from openapi.db.models.namespace import Namespace

log = Logger('db/project')

class Project(db.Entity):

    _table_ = 'project'

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    user = Required(str)
    openapi_info = Required(Json)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime,  nullable=True)
    info = Optional(Json)
    latest = Required(bool, default=True)
    namespace = Required(Namespace)

    @classmethod
    @db_session
    def create(cls, namespace_id, body, user):
        obj =  get(n for n in Project if n.namespace.id == namespace_id and n.delete_at == None and
                   n.openapi_info['title'] == body.get('title') and n.openapi_info['verison'] != body.get('version'))
        if obj:
            raise IsExist(title='不能创建同名的项目', detail=f'已经存在，uid为{obj.uid}')
        obj = get(n for n in Project if n.namespace.id == namespace_id and n.delete_at == None and
                   n.openapi_info['title'] == body.get('title') and n.openapi_info['version'] == body.get('version'))
        if obj:
            raise IsExist(title='此项目的版本已经存在', detail=f'已经存在，uid为{obj.uid}')
        obj = get(n for n in Project if n.namespace.id == namespace_id and n.delete_at == None and
                  n.openapi_info['title'] == body.get('title') and n.latest == True)
        if obj:
            obj.latest = False
        Project(openapi_info=body, user=user, namespace=namespace_id)

    @classmethod
    @db_session
    def list(cls, namespace_id, version):
        if version:
            objs = select(n for n in Project if n.namespace.id == namespace_id and n.namespace.delete_at == None and
                          n.openapi_info['version'] == version).order_by(desc(Project.id))
        else:
            objs = select(n for n in Project if n.namespace.id == namespace_id and n.namespace.delete_at == None and
                          n.latest == True).order_by(desc(Project.id))
        data = []
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'uid': obj.uid,
                'openapi_info': obj.openapi_info
            }
            data.append(tmp_dict)
        return data

    @classmethod
    @db_session
    def update_project_by_id(cls, namespace_id, project_id, body, user):
        obj = get(n for n in Project if n.id == project_id and n.delete_at == None and n.namespace.id == namespace_id
                     and n.namespace.delete_at == None)
        if obj:
            project = obj.openapi_info['title']
            version = obj.openapi_info['version']
            if project != body.get('title'):
                raise DefalutError(title='不能修改项目名', detail=f'不能将项目名{project}修改为{body.get("title")}')
            if version != body.get('version'):
                raise DefalutError(title='不能修改版本号', detail=f'不能修改项目{project}的版本号从{version}到{body.get("version")}')
            obj.openapi_info = body
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')
