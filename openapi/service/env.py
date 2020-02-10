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