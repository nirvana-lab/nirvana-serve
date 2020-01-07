# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from openapi.service import component

def list():
    pass


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