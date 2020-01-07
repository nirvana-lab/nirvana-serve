#-*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import uuid
import datetime
from openapi.utils.exception_handle import IsExist, DefalutError, IsNotExist
from logbook import Logger
from openapi.db.models.project import Project

log = Logger('db/component')

class Component(db.Entity):
    _table_ = 'component'

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    component = Required(str)
    component_content = Required(Json)
    type = Required(str)
    user = Required(str)
    info = Optional(Json)
    project = Required(Project)

    @classmethod
    @db_session
    def create(cls, namespace_id, project_id, component_content, component, type, user):
        obj = get(n for n in Component if n.component == component and n.delete_at == None and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None
                  and n.type == type)
        if obj:
            raise IsExist(title='不能创建同名的Component', detail=f'类型为{type}的Component已经存在，uid为{obj.uid}')
        else:
            Component(component=component, component_content=component_content, type=type, user=user, project=project_id)

    @classmethod
    @db_session
    def list(cls, namespace_id, project_id):
        data = []
        objs = select(n for n in Component if n.delete_at == None and
                      n.project.id == project_id and n.project.delete_at == None and
                      n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None)
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'uid': obj.uid,
                'type': obj.type,
                'component_content': obj.component_content
            }
            data.append(tmp_dict)
        return data

    @classmethod
    @db_session
    def get_detail_by_id(cls, namespace_id, project_id, component_id):
        obj = get(n for n in Component if n.delete_at == None and n.id == component_id and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None)
        if obj:
            return {
                'id': obj.id,
                'uid': obj.uid,
                'type': obj.type,
                'component_content': obj.component_content
            }
        else:
            raise IsNotExist(title='Component不存在', detail=f'id为{component_id}的Component不存在')


    @classmethod
    @db_session
    def update_component_by_id(cls, namespace_id, project_id, component_id, component, component_content, user):
        obj = get(n for n in Component if n.delete_at == None and  n.id == component_id and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None)
        if obj:
            if obj.component == component:
                obj.component_content = component_content
                obj.user = user
                obj.update_at = datetime.datetime.utcnow()
            else:
                raise DefalutError(title='不能修改Component名', detail=f'不能将Component名{obj.component}修改为{component}')
        else:
            raise IsNotExist(title='Component不存在', detail=f'id为{component_id}的Component不存在')


    @classmethod
    @db_session
    def delete_api_by_id(cls, namespace_id, project_id, component_id, user):
        obj = get(n for n in Component if n.delete_at == None and n.delete_at == None and n.id ==component_id and
                  n.project.id == project_id and n.project.delete_at == None and
                  n.project.namespace.id == namespace_id and n.project.namespace.delete_at == None)
        if obj:
            obj.delete_at = datetime.datetime.utcnow()
            obj.user = user
        else:
            raise IsNotExist(title='Component不存在', detail=f'id为{component_id}的Component不存在')