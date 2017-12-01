""" OpenAPI documents """


import yaml


def build(settings, resources_tree):
    """ Build RAML document for the resources
    """
    document_dict = _build_dict(settings, resources_tree)
    document = '\n'.join([
        '{}'.format(yaml.dump(document_dict)),
    ])
    return document


def _build_dict(settings, resources_tree):
    document_dict = {
        'openapi': '3.0.0',
        'info': {
            'title': settings['rapids.title'],
        },
        'paths': {},
    }
    document_dict['paths'].update(_add(resources_tree))
    return document_dict


def _add(resources_tree, parent_class=None):
    document_tree = {}
    for resource_config in resources_tree.get(parent_class, {}).values():
        node = {}
        for (method, conf) in resource_config.get('methods', {}).items():
            node[method] = conf
        uri_parameters_config = resource_config['uri_parameters']
        if uri_parameters_config:
            parameters = node.setdefault('parameters', [])
            for (name, conf) in uri_parameters_config.items():
                parameters.append({
                    'name': name,
                    'in': 'path',
                    'required': True,  # optional URI parameters unsupported
                    'schema': {
                        'type': conf['type'],
                    },
                })
        node.update(_add(resources_tree, resource_config['resource_class']))
        uri_segment_pattern = '/{}'.format(
            resource_config['uri_segment_pattern'],
        )
        document_tree[uri_segment_pattern] = node
    return document_tree


# EOF
