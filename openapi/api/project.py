# -*- coding: utf-8 -*-
import connexion
from openapi.service import project
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist

def list(namespace_id, version=None):
    '''
    API接口：获取项目的列表
    :param namespace_id: namespace的id
    :return: 返回的项目的列表
    '''
    try:
        data = project.project_list(namespace_id, version)
        return {
            'data': data
        }, 200
    except Exception as e:
        raise DefalutError(title=f'获取项目列表异常', detail=f'{e}')

def create(namespace_id, body):
    '''
    API接口: 根据接口内容创建项目
    :param namespace_id: namespace的id
    :param body: 创建项目的请求体
    :return: 返回创建成功信息
    '''
    try:
        user = connexion.request.headers.get('user')
        project_name = project.create_project(namespace_id, body, user)
        return {
                   'title': f'创建项目成功',
                   'detail': f'创建项目: {project_name}成功'
               }, 201
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'创建项目异常', detail=f'{e}')

def update(namespace_id, project_id, body):
    '''
    API接口： 更新项目内容
    :param namespace_id: namespace的id
    :param project_id: project的id
    :param body: 更新项目的请求体
    :return: 返回更新成功的信息
    '''
    try:
        user = connexion.request.headers.get('user')
        project.update_project_by_id(namespace_id, project_id, body, user)
        return {
            'title': '更新项目成功',
            'detail': f'更新项目id为{project_id}的项目成功'
        }, 200
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'更新项目异常', detail=f'{e}')

def delete(namespace_id, project_id):
    '''
    API接口： 删除指定的项目
    :param namespace_id: namespace的id
    :param project_id: project的id
    :return: 返回删除成功的信息
    '''
    try:
        user = connexion.request.headers.get('user')
        project.delete_project_by_id(namespace_id, project_id, user)
        return {
            'title': '删除项目成功',
            'detail': f'删除项目id为{project_id}的项目成功'
        }, 200
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'删除项目异常', detail=f'{e}')