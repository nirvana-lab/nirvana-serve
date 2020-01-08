# -*- coding: utf-8 -*-
from openapi.db.models.namespace import Namespace
from logbook import Logger

log = Logger('service/namespace')

def create_namespace(body, user):
    '''
    :param body: 创建namespace接口的body
    :param user: 创建namespace的用户
    :return: 返回被创建namespace的名字
    '''
    namespace = body.get('name')
    description = body.get('description')
    Namespace.create(namespace, description, user)
    return namespace


def namespace_list():
    '''
    :return: 返回namespace的列表
    '''
    return Namespace.list()


def delete_namespace(namespace_id, user):
    '''

    :param namespace_id: 删除的namespace的id
    :param user: 操作人
    :return:
    '''
    Namespace.delete_namespace_by_id(namespace_id, user)