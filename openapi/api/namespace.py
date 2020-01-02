# -*- coding: utf-8 -*-
import connexion
from openapi.service.namespace import create_namespace, namespace_list
from openapi.utils.exception_handle import DefalutError, IsExist

def list():
    '''
    API接口: 获取namesapce的列表
    :return: 返回namespace的列表
    '''
    try:
        data = namespace_list()
        return {
            'data': data
        }, 200
    except Exception as e:
        raise DefalutError(title=f'获取namespace列表异常', detail=f'{e}')

def create(body):
    '''
    API接口：创建namespace
    :param body: 创建namespace的请求体
    :return: 返回创建成功信息
    '''
    try:
        user = connexion.request.headers.get('user')
        namespace = create_namespace(body, user)
        return {
            'title': f'创建namespace成功',
            'detail': f'创建namespace: {namespace}成功'
        }, 201
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'创建namespace异常', detail=f'{e}')
