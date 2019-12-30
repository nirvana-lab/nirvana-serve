# -*- coding: utf-8 -*-
from openapi.db.models.namespace import Namespace
from logbook import Logger

log = Logger('service/namespace')

def create_namespace(body, user):
    '''
    :param body: 创建namespace接口的body
    :param user: 创建namespace的用户
    :return: 无
    '''
    namespace = body.get('namespace')
    description = body.get('description')
    Namespace.create(namespace, description, user)


def namespace_list():
    '''
    :return: 返回namespace的列表
    '''
    return Namespace.list()