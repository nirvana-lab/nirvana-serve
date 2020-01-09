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
    info = Optional(Json)
    namespace = Required(Namespace)

    @classmethod
    @db_session
    def create(cls, namespace_id, project_content, user):
        Project(project_content=project_content, user=user, namespace=namespace_id)


    @classmethod
    @db_session
    def get_project_list_by_namespace_id(cls, namespace_id):
        print(namespace_id)
        data = []
        objs = select(n for n in Project if n.delete_at == None and n.namespace.id == namespace_id
                      and n.namespace.delete_at == None)
        for obj in objs:
            content = obj.project_content
            tmp_dict = {
                'id': obj.id,
                'name': content.get('detail').get('info').get('title'),
                'description': content.get('detail').get('info').get('description')
            }
            data.append(tmp_dict)
        return data

