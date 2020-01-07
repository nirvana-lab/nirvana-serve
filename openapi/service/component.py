# -*- coding: utf-8 -*-
from openapi.db.models.component import Component
from logbook import Logger

log = Logger('service/component')

def create_component(namespace_id, project_id, body, user):
    type = body.get('type')
    component_content = body.get('component_content')
    component = list(component_content.keys())[0]
    Component.create(namespace_id, project_id, component_content, component, type, user)