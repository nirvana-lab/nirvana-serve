# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist
from openapi.service import user

def login(body):
    '''
    API接口
    :param body: 登陆用户的内容
    :return: 返回登陆的结果
    '''
    try:
        auth = user.login(body)
        return {
            'title': '登陆成功',
            'detail': '登陆成功',
            'auth': auth
        }, 200
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'登陆异常', detail=f'{e}')


def register(body):
    '''
    API接口
    :param body:  注册用户的内容
    :return: 返回注册的结果
    '''
    try:
        user.register(body)
        return {
            'title': '注册用户成功',
            'detail': '注册用户成功'
        }
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'注册用户异常', detail=f'{e}')