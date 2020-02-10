#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from flask_cors import CORS
from logbook import Logger
# from flask import request
from openapi.config.config import check_config_path
from flask import g

from openapi.utils.log_handle import setup_logger
from openapi.utils.problem_handle import problem_exception_handler, exception_handler
from openapi.utils.exception_handle import DefalutError
from openapi.db.db import db
from openapi.utils.auth_handle import check_token
from openapi.db.models.user import User # noqa: F401
from openapi.db.models.namespace import Namespace # noqa: F401
from openapi.db.models.project import Project # noqa: F401
# from openapi.db.models.api import Api # noqa: F401
# from openapi.db.models.component import Component # noqa: F401
from openapi.db.models.env import Env # noqa: F401
# from openapi.db.models.var_global import VarGlobal # noqa: F401
# from openapi.db.models.script import Script
# from openapi.db.models.case import Case
# from openapi.db.models.history import History
# from openapi.db.models.task import Task
# from openapi.db.models.task_histroy import TaskHistory

# from flask import Flask
# from flask_socketio import SocketIO

if __name__ == '__main__':
    setup_logger()
    log = Logger('dx-captian')
    log.info('database mapping generating')
    db.generate_mapping(create_tables=True)
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='specs/')
    CORS(app.app)
    app.add_api('openapi.yaml', arguments={'title': 'api'})
    log.info('api.yaml loaded!')
    log.info('file.yaml loaded!')
    app.add_error_handler(connexion.ProblemException, problem_exception_handler)
    app.add_error_handler(Exception, exception_handler)
    log.info('error handler added')
    check_config_path()

    @app.app.before_request
    def before():
        if connexion.request.path == '/api/register' or connexion.request.path == '/api/login'\
                or connexion.request.path == '/api/ui/' or connexion.request.path == '/api/openapi.json'\
                or connexion.request.path == '/api/ui/favicon-32x32.png'\
                or connexion.request.path == '/favicon.ico' or '/api/ui/' in connexion.request.path:
            pass
        else:
            user = check_token(connexion.request.headers.get('token'))
            if user:
                g.username = user
            else:
                raise DefalutError(title=f'验证失败', detail=f'验证失败', status=401, type='AuthError')

    app.run(host='0.0.0.0', debug=True)

    # socket_app = Flask(__name__)
    # socketio = SocketIO(socket_app)
