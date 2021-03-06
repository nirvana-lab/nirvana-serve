# -*- coding: utf-8 -*-
from openapi.db.models.namespace import Namespace
from openapi.db.models.project import Project
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


def namespace_list(is_include_project):
    '''
    :param is_include_project: 返回内容是否需要包含项目内容
    :return: 返回namespace的列表
    '''
    datas = Namespace.list()

    if is_include_project == "True":
        for data in datas:
            project_data = Project.get_project_list_by_namespace_id(data.get('id'))
            data['projects'] = project_data
    return datas


def delete_namespace(namespace_id, user):
    '''

    :param namespace_id: 删除的namespace的id
    :param user: 操作人
    :return:
    '''
    Namespace.delete_namespace_by_id(namespace_id, user)


def get_namespace_detail_by_id(namespace_id):
    '''

    :param namespace_id: 被指定的namespace
    :return:
    '''
    datas = Namespace.get_namespace_detail_by_id(namespace_id)
    for data in datas:
        project_data = Project.get_project_list_by_namespace_id(data.get('id'))
        data['projects'] = project_data
    return datas