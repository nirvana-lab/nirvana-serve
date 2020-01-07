# -*- coding: utf-8 -*-
from openapi.db.models.component import Component
from logbook import Logger

log = Logger('service/component')

def create_component(namespace_id, project_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 创建component的body
    :param user: 创建component的用户
    :return:
    '''
    type = body.get('type')
    component_content = body.get('component_content')
    component = list(component_content.keys())[0]
    Component.create(namespace_id, project_id, component_content, component, type, user)


def component_list(namespace_id, project_id):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :return: 返回component的列表
    '''
    return Component.list(namespace_id, project_id)


def get_detail_by_id(namespace_id, project_id, component_id):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param component_id: component的id
    :return: 返回component的详情
    '''
    return Component.get_detail_by_id(namespace_id, project_id, component_id)


def update_component_by_id(namespace_id, project_id, component_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param component_id: component的id
    :param body: 更新component的内容
    :param user: 更新component的用户
    :return:
    '''
    component_content = body.get('component_content')
    component = list(component_content.keys())[0]
    Component.update_component_by_id(namespace_id, project_id, component_id, component, component_content, user)

def delete_component_by_id(namespace_id, project_id, component_id, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param component_id: component的id
    :param user: 删除component的用户
    :return:
    '''
    Component.delete_api_by_id(namespace_id, project_id, component_id, user)