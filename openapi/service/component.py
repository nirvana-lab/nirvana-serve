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