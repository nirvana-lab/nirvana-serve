# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from openapi.service import component

def list(namespace_id, project_id):
    '''
    API接口：获取项目下的Component列表
    :param namespace_id: namespace的id
    :param project_id: project的id
    :return: 返回Component列表
    '''
    try:
        data = component.component_list(namespace_id, project_id)
        return {
            'data': data
        }, 200
    except Exception as e:
        raise DefalutError(title=f'获取Component列表异常', detail=f'{e}')


def create(namespace_id, project_id, body):
    '''
    API接口：在项目下创建Component
    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 创建component的内容
    :return:
    '''
    try:
        user = connexion.request.headers.get('user')
        component.create_component(namespace_id, project_id, body, user)
        return {
            'title': '创建component成功',
            'detail': '创建component成功'
        }, 200
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'创建Component异常', detail=f'{e}')

def detail(namespace_id, project_id, component_id):
    '''
    API接口：获取指定Component的详情
    :param namespace_id: namespace的id
    :param project_id: project的id
    :param component_id: component的id
    :return: 返回Component的详情
    '''
    try:
        data = component.get_detail_by_id(namespace_id, project_id, component_id)
        return data, 200
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'获取Component详情异常', detail=f'{e}')