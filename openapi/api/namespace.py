# -*- coding: utf-8 -*-
import connexion
from openapi.service.namespace import create_namespace, namespace_list, delete_namespace, get_namespace_detail_by_id
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g

def list(project="True"):
    '''
    API接口: 获取namesapce的列表
    :param project: 根据project来判断返回接口是否需要显示项目的具体内容，默认为需要显示
    :return: 返回namespace的列表
    '''
    try:
        data = namespace_list(is_include_project=project)
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
        namespace = create_namespace(body, g.username)
        return {
            'title': f'创建namespace成功',
            'detail': f'创建namespace: {namespace}成功'
        }, 201
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'创建namespace异常', detail=f'{e}')

def delete(namespace_id):
    '''
    API接口：删除指定的namespace
    :param namespace_id: 要被删除的namespace的id
    :return:
    '''
    try:
        delete_namespace(namespace_id, g.username)
        return {
            'title': '删除namespace成功',
            'detail': '删除namespace成功'
        }, 200
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'删除namespace异常', detail=f'{e}')


def detail(namespace_id):
    '''

    :param namespace_id: 被指定的namespace
    :return:
    '''
    try:
        data = get_namespace_detail_by_id(namespace_id)
        return {
            'data': data
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'根据namespace_id获取详情异常', detail=f'{e}')