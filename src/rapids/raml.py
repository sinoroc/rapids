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
    for resource in resources_tree.get(parent_class, {}).values():
        uri_segment_pattern = '/{}'.format(resource['uri_segment_pattern'])
        node = {}
        for (method, conf) in resource.get('methods', {}).items():
            node[method] = conf
        node.update(_add(resources_tree, resource['resource_class']))
        document_tree[uri_segment_pattern] = node
    return document_tree


# EOF
