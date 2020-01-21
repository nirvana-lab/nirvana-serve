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
        data = project.create_project(namespace_id, body, g.username)
        return {
            'data': data
        }
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
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

def delete(project_id):
    '''
    API接口: 删除项目
    :param project_id: 删除项目的id
    :return:
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        project.delete_project(namespace_id, project_id, g.username)
        return {
            'title': '删除项目成功',
            'detail': '删除项目成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'删除项目详情异常', detail=f'{e}')

def rename(project_id, body):
    '''
    API接口：重命名项目名
    :param project_id: 项目的id
    :param body: 项目重命名的内容
    :return:
    '''
    try:
        namespace_id = connexion.request.headers.get('namespace')
        project.project_rename_by_id(namespace_id, project_id, body, g.username)
        return {
            'title': '项目重命名成功',
            'detail': '项目重命名成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'项目名重命名异常', detail=f'{e}')