# -*- coding: utf-8 -*-
from openapi.db.models.project import Project
from logbook import Logger

log = Logger('service/project')

def create_project(namespace_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param body: 创建项目的body
    :param user: 创建项目的用户
    :return:
    '''
    Project.create(namespace_id, body, user)
