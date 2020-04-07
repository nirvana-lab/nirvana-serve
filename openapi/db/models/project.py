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
    project_content = Required(Json)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime,  nullable=True)
    swagger_json = Optional(Json, nullable=True)
    info = Optional(Json)
    namespace = Required(Namespace)

    @classmethod
    @db_session
    def create(cls, namespace_id, project_content, user):
        project = Project(project_content=project_content, user=user, namespace=namespace_id)
        return project

    @classmethod
    @db_session
    def create_by_swagger(cls, namespace_id, project_content, swagger_json, user, url):
        Project(project_content=project_content, swagger_json=swagger_json, user=user, namespace=namespace_id, info={"url": url})


    @classmethod
    @db_session
    def sync_swagger_by_id(cls, namespace_id, project_content, swagger_json, user, project_id):
        obj = get(n for n in Project if n.delete_at == None and n.id == project_id and
                  n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            obj.project_content = project_content
            obj.swagger_json = swagger_json
            obj.user= user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')

    @classmethod
    @db_session
    def get_project_list_by_namespace_id(cls, namespace_id):
        data = []
        objs = select(n for n in Project if n.delete_at == None and n.namespace.id == namespace_id
                      and n.namespace.delete_at == None).order_by(Project.id)
        for obj in objs:
            content = obj.project_content
            tmp_dict = {
                'id': obj.id,
                'name': content.get('detail').get('info').get('title'),
                'description': content.get('detail').get('info').get('description'),
                'tag': content.get('tag'),
                'commit': content.get('commit')
            }
            data.append(tmp_dict)
        return data


    @classmethod
    @db_session
    def get_project_detail_by_id(cls, namespace_id, project_id):
        obj = get(n for n in Project if n.id == project_id and n.delete_at == None
                  and n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            return obj.project_content
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')


    @classmethod
    @db_session
    def update_project_by_id(cls, namespace_id, project_id, project_content, user):
        obj = get(n for n in Project if n.id == project_id and n.delete_at == None
                  and n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
            obj.project_content = project_content
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')


    @classmethod
    @db_session
    def delete_project_by_id(cls, namespace_id, project_id, user):
        obj = get(n for n in Project if n.id == project_id and n.delete_at == None and
                  n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            obj.delete_at = datetime.datetime.utcnow()
            obj.user = user
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')


    @classmethod
    @db_session
    def rename_project_by_id(cls, namespace_id, project_id, new_name, user):
        obj = get(n for n in Project if n.id == project_id and n.delete_at == None
                  and n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            content = obj.project_content
            content['detail']['info']['title'] = new_name
            obj.project_content = content
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')

    @classmethod
    @db_session
    def retag_project_by_id(cls, namespace_id, project_id, new_tag, user):
        obj = get(n for n in Project if n.id == project_id and n.delete_at == None
                  and n.namespace.id == namespace_id and n.namespace.delete_at == None)
        if obj:
            content = obj.project_content
            content['tag'] = new_tag
            obj.project_content = content
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='项目不存在', detail=f'id为{project_id}的项目不存在')