# -*- coding: utf-8 -*-
from openapi.db.models.api import Api
from logbook import Logger

log = Logger('service/api')

def create_api(namespace_id, project_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 创建接口的body
    :param user: 创建project的用户
    :return:
    '''
    path = list(body.keys())[0]
    method = list(body.get(path).keys())[0]
    Api.create(namespace_id, project_id, body, method, path, user)


def api_list(namespace_id, project_id):
    '''

    :param namespace_id: namespace的id
    :param project_id: project的id
    :return: 接口列表
    '''
    return Api.list(namespace_id, project_id)