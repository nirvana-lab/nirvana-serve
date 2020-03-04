# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g
from urllib.parse import urlparse, parse_qs, urlsplit

def post(namespace_id, project_id, path, body):
    print(namespace_id)
    print(project_id)
    print(path)
    print(body)
    print(connexion.request.headers)
    print(connexion.request.parameter_storage_class)
    print(connexion.request.url)
    print(connexion.request.path)
    result = urlparse(url=connexion.request.url)
    print(result)

    result = parse_qs(urlsplit(connexion.request.url).query)
    print(result)
