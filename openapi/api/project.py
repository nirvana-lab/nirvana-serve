# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from openapi.service import project
from flask import g

def create(body):
    '''
    API接口
    :param body: 创建项目的body
    :return:
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        project.create_project(namespace_id, body, g.username)
        return {
            'title': '创建项目成功',
            'detail': '创建项目成功'
        }
    except Exception as e:
        raise DefalutError(title=f'创建项目异常', detail=f'{e}')