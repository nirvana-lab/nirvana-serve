# -*- coding: utf-8 -*-
from openapi.db.models.project import Project
from logbook import Logger
from openapi.utils.exception_handle import DefalutError

log = Logger('service/project')

def create_project(namespace_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param body: 创建项目的body
    :param user: 创建项目的用户
    :return:
    '''
    tag = body.get('tag')
    if '$' in tag:
        raise DefalutError(title='tag中不能包含字符$', detail=f'tag为{tag}')
    project = Project.create(namespace_id, body, user)
    data = {
        'id': project.id,
        'name': body.get('detail').get('info').get('title'),
        'description': body.get('detail').get('info').get('description'),
        'tag': tag
    }
    return data

def project_detail(namespace_id, project_id):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :return: 返回项目详情
    '''
    return Project.get_project_detail_by_id(namespace_id, project_id)


def update_project(namespace_id, project_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 更新项目的内容
    :param user: 操作人
    :return:
    '''
    Project.update_project_by_id(namespace_id, project_id, body, user)

def delete_project(namespace_id, project_id, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
     :param user: 操作人
    :return:
    '''
    Project.delete_project_by_id(namespace_id, project_id, user)