""" RAML documents
"""


import yaml


def build(settings, resources_tree):
    """ Build RAML document for the resources
    """
    document_dict = _build_dict(settings, resources_tree)
    document = '\n'.join([
        '#%RAML 1.0',
        '---',
        '{}'.format(yaml.dump(document_dict)),
        '...  # EOF',
    ])
    return document


def _build_dict(settings, resources_tree):
    document_dict = {
        'title': settings['rapids.title'],
    }
    document_dict.update(_add(resources_tree))
    return document_dict


def _add(resources_tree, parent_class=None):
    document_tree = {}
    for resource_config in resources_tree.get(parent_class, {}).values():
        uri_segment_pattern = '/{}'.format(
            resource_config['uri_segment_pattern'],
        )
        node = {}
        uri_parameters_config = resource_config['uri_parameters']
        if uri_parameters_config:
            node['uriParameters'] = uri_parameters_config
        for (method, conf) in resource_config.get('methods', {}).items():
            node[method] = conf
        node.update(_add(resources_tree, resource_config['resource_class']))
        document_tree[uri_segment_pattern] = node
    return document_tree


# EOF
