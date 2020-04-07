from logbook import Logger
from openapi.utils.exception_handle import DefalutError
import requests
import json
import copy
from openapi.db.models.project import Project
import yaml
import re

log = Logger('service/swagger')
nirvana_json_format = {
    'tag': "swagger_json",
    'apis': [],
    'envs': [],
    'detail': {
        'info': {
            'title': '',
            'version': '',
            'description': ''
        },
        'tags': [],
        'servers': []
    },
    'models': [],
    'scripts': []
}

def import_swagger_by_url(namespace_id, body, user):
    try:
        url = body.get('url')
        resp = requests.get(url)
        swagger_content = check_swagger_type(resp.content)
    except Exception as e:
        raise DefalutError(title='获取swagger_json失败', detail=f'{e}')
    nirvana_json = swagger_json_change_to_nirvana_json(swagger_content)
    if body.get('tag'):
        nirvana_json['tag'] = body.get('tag')
    Project.create_by_swagger(namespace_id, nirvana_json, swagger_content, user, url)


def check_swagger_type(content):
    tmp_content = None
    try:
        tmp_content = yaml.load(content)
        flag = True
    except:
        flag = False

    try:
        if not flag:
            tmp_content = json.loads(content)
            flag = True
    except:
        flag = False

    if flag:
        return tmp_content
    else:
        raise DefalutError(title='导入swagger失败', detail='导入内容格式不是json，也不是yaml', type='SwaggerError')


def swagger_json_change_to_nirvana_json(swagger_json):
    swagger_info = swagger_json.get('info')
    swagger_servers = swagger_json.get('servers')
    swagger_tags = swagger_json.get('tags')


    tmp_data = copy.deepcopy(nirvana_json_format)

    if swagger_info:
        tmp_data['detail']['info'] = swagger_info
    if swagger_servers:
        tmp_data['detail']['servers'] = swagger_servers
    if swagger_tags:
        tmp_data['detail']['tags'] = swagger_tags

    swagger_paths = swagger_json.get('paths')
    tmp_data['apis'] = paths_change(swagger_paths)
    try:
        swagger_components = swagger_json.get('components').get('schemas')
        if swagger_components:
            swagger_components_fix_ref = ref_format(swagger_components)
            model_list = model_change(swagger_components_fix_ref)
            tmp_data['models'] = model_list
    except:
        pass
    return tmp_data

def paths_change(swagger_paths):
    tmp_list = []
    for path in swagger_paths.keys():
        for method in swagger_paths[path].keys():
            tmp_dict = {
                'tags': [],
                'query': [],
                'header': [],
                'method': '',
                'params': [],
                'description': '',
                'requestBody': '',
                'responseBody': []
            }
            tmp_dict['path'] = path
            tmp_dict['method'] = method
            if 'tags' in swagger_paths[path][method].keys():
                tmp_dict['tags'] = swagger_paths[path][method]['tags']
            if 'summary' in swagger_paths[path][method].keys():
                tmp_dict['description'] = swagger_paths[path][method]['summary']
            if 'parameters' in swagger_paths[path][method].keys():
                tmp_query_list = []
                tmp_header_list = []
                tmp_path_list = []

                for param in swagger_paths[path][method]['parameters']:
                    tmp_param_dict = {}
                    tmp_param_dict['key'] = param.get('name')
                    tmp_param_dict['type'] = param.get('schema').get('type')
                    tmp_param_dict['value'] = param.get('value')
                    tmp_param_dict['require'] = param.get('required')
                    tmp_param_dict['description'] = param.get('description')

                    if param['in'] == 'header':
                        tmp_header_list.append(tmp_param_dict)
                    elif param['in'] == 'query':
                        tmp_query_list.append(tmp_param_dict)
                    elif param['in'] == 'path':
                        tmp_path_list.append(tmp_param_dict)
                if tmp_query_list:
                    tmp_dict['query'] = tmp_query_list
                if tmp_header_list:
                    tmp_dict['header'] = tmp_header_list
                if tmp_path_list:
                    tmp_dict['params'] = tmp_path_list
            if 'requestBody' in swagger_paths[path][method].keys():
                if 'application/json' in swagger_paths[path][method].get('requestBody').get('content').keys():
                    requsetBody_content = swagger_paths[path][method].get('requestBody').get('content').get('application/json').get('schema')
                elif 'multipart/form-data' in swagger_paths[path][method].get('requestBody').get('content').keys():
                    requsetBody_content = swagger_paths[path][method].get('requestBody').get('content').get(
                        'multipart/form-data').get('schema')
                else:
                    requsetBody_content = None
                requestBody_content_fix_ref = ref_format(requsetBody_content)

                tmp_dict['requestBody'] = yaml.safe_dump(requestBody_content_fix_ref, default_flow_style=False, allow_unicode=True)
            if 'responses' in swagger_paths[path][method].keys():
                response_list = []
                for k, v in swagger_paths[path][method]['responses'].items():
                    tmp_response_dict = {
                        'code': k,
                        'description': None,
                        'content': None
                    }
                    if 'description' in swagger_paths[path][method]['responses'][k]:
                        tmp_response_dict['description'] = v.get('description')
                    if 'content' in swagger_paths[path][method]['responses'][k]:
                        for content_k, content_v in v.get('content').items():
                            if content_k == 'application/json':
                                responses_content = v.get('content').get('application/json').get('schema')
                                responses_content_fix_ref = ref_format(responses_content)
                                tmp_response_dict['content'] = yaml.safe_dump(responses_content_fix_ref, default_flow_style=False, allow_unicode=True)
                            elif 'text/plain' in content_k:
                                tmp_response_dict['content'] = v.get('content').get(content_k).get('schema')
                    response_list.append(tmp_response_dict)
                if response_list:
                    tmp_dict['responseBody'] = response_list
            tmp_list.append(tmp_dict)
    return tmp_list


def model_change(swagger_components):
    re_list = []
    for k, v in swagger_components.items():
        tmp_dict = {}
        tmp_dict['name'] = k
        tmp_dict['body'] = yaml.safe_dump(v, default_flow_style=False, allow_unicode=True)
        tmp_dict['description'] = ''
        re_list.append(tmp_dict)
    return re_list


def ref_format(content):
    content_str = json.dumps(content)
    check_flag = True

    while check_flag:
        search_result = re.search("\"\$ref\": \"#/components/schemas/\w+\"", content_str)
        if search_result:
            tmp_str = content_str[search_result.start():search_result.end()]
            tmp_replace = tmp_str.split('/')[-1][:-1]
            content_str = content_str[:search_result.start()] + '"type": "${' + tmp_replace + '}"' +  content_str[search_result.end():]
        else:
            check_flag = False
    return json.loads(content_str)

