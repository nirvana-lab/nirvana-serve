# -*- coding: utf-8 -*-
from openapi.db.models.project import Project
from logbook import Logger

log = Logger('service/project')


def create_project(namespace_id, body, user):
    '''
    :param namespace_id: namespace的id
    :param body:  创建project接口的body
    :param user:  创建project的用户
    :return:
    '''
    project = body.get('title')
    Project.create(namespace_id, body, user)
    return project

def project_list(namespace_id, version):
    '''

    :param namespace_id: namespace的id
    :return: 返回项目列表
    '''
    return Project.list(namespace_id, version)

def update_project_by_id(namespace_id, project_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 更新project的body
    :param user: 更新project的用户
    :return:
    '''
    Project.update_project_by_id(namespace_id, project_id, body, user)

def delete_project_by_id(namespace_id, project_id, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param user: 删除项目的用户
    :return:
    '''
    Project.delete_project_by_id(namespace_id, project_id, user)
