# -*- coding: utf-8 -*-
import connexion
from openapi.service import api
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist

def list(namespace_id, project_id):
    '''
    API接口：获取接口列表
    :param namespace_id: namespace的id
    :param project_id: project的id
    :return: 返回接口列表
    '''
    try:
        data = api.api_list(namespace_id, project_id)
        return {
            'data': data
        }, 200
    except Exception as e:
        raise DefalutError(title=f'获取接口列表异常', detail=f'{e}')

def create(namespace_id, project_id, body):
    '''
    API接口： 创建API接口
    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 创建Api的请求体body
    :return:
    '''
    try:
        user = connexion.request.headers.get('user')
        api.create_api(namespace_id, project_id, body, user)
        return {
            'title': '创建接口成功',
            'detail': '创建接口成功'
        }, 201
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'创建接口异常', detail=f'{e}')