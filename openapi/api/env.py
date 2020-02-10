# -*- coding: utf-8 -*-
import connexion
from openapi.service import env
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g

def list():
    '''
    API接口：或者指定namespace下的环境列表
    :return: 环境列表
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        data = env.env_list(namespace_id)
        return {
            'data': data
        }
    except Exception as e:
        raise DefalutError(title=f'获取环境列表异常', detail=f'{e}')

def create(body):
    '''
    API接口：创建环境
    :param body: 创建环境的body
    :return:
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        env.create_env(namespace_id, body, g.username)
        return {
            'title': '创建环境成功'
        }
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'创建环境异常', detail=f'{e}')

def update(env_id, body):
    '''
    API接口: 更新环境内容
    :param body: 更新环境内容的body
    :return:
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        env.update_env(namespace_id, env_id, body, g.username)
        return {
            'title': '更新环境成功'
        }
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'更新环境异常', detail=f'{e}')


def delete(env_id):
    pass