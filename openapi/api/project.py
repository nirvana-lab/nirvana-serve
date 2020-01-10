# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from openapi.service import project
from flask import g

def create(body):
    '''
    API接口： 创建项目
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


def detail(project_id):
    '''
    API接口：获取项目的详情
    :param project_id: 获取项目详情的id
    :return: 指定项目的详情
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        return project.project_detail(namespace_id, project_id)
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'获取项目详情异常', detail=f'{e}')


def update(project_id, body):
    '''
    API接口: 更新项目的详情
    :param project_id: 更新项目详情的id
    :param body: 更新项目的详情
    :return:
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        project.update_project(namespace_id, project_id, body, g.username)
        return {
            'title': '更新项目成功',
            'detail': '更新项目成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'更新项目详情异常', detail=f'{e}')