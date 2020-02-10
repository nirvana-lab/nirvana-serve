# -*- coding: utf-8 -*-
import connexion
from openapi.service import env
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g

def list():

    pass

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