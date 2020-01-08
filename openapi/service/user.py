# -*- coding: utf-8 -*-
from openapi.db.models.user import User
from logbook import Logger
from openapi.utils import auth_handle
import uuid

log = Logger('service/user')


def register(body):
    '''

    :param body: 注册用户的内容
    :return:
    '''
    username = body.get('username')
    password = body.get('password')
    User.register(username, password)


def login(body):
    '''

    :param body: 登陆用户的内容
    :return: 返回jwt
    '''
    username = body.get('username')
    password = body.get('password')
    uid = User.login(username, password)

    jwt_token = auth_handle.generate_jwt_token(username, uid)

    return jwt_token


def check_user_valid(user, uid):
    '''

    :param user: 用户名
    :param uid: uid
    :return:
    '''
    uid = uuid.UUID(uid)
    return User.user_is_valid(user, uid)
