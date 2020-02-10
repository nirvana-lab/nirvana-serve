# -*- coding: utf-8 -*-
from openapi.db.models.env import Env
from logbook import Logger
from openapi.utils.exception_handle import DefalutError

log = Logger('service/env')

def create_env(namespace_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param body: 创建环境的body
    :param user: 创建项目的用户
    :return:
    '''
    env = body.get('env')
    url = body.get('url')
    description = body.get('description')

    Env.create(namespace_id, env, url, description, user)


def env_list(namespace_id):
    return Env.list(namespace_id)


def update_env(namespace_id, env_id, body, user):
    '''

    :param namespace_id: namespace的id
    :param env_id: namespace的id
    :param body: 更新环境的body
    :param user: 更新环境的用户
    :return:
    '''
    env = body.get('env')
    url = body.get('url')
    description = body.get('description')
    Env.update(namespace_id, env_id, env, url, description, user)


def delet_env(namespace_id, env_id, user):
    '''

    :param namespace_id: namespace的id
    :param env_id: env的id
    :param user: 删除环境的用户
    :return:
    '''
    Env.delete(namespace_id, env_id, user)