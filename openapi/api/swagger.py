# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from openapi.service import swagger
from flask import g

def url(body):
    try:
        namespace_id = connexion.request.headers.get('namespace')
        swagger.import_swagger_by_url(namespace_id, body, g.username)
        return {
            'title': '导入swagger成功',
            'detail': '导入swagger成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'导入swagger异常', detail=f'{e}')

def sync(project_id):
    try:
        pass
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}', type=f'{e.type}')
    except Exception as e:
        raise DefalutError(title=f'同步swagger异常', detail=f'{e}')