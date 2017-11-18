""" RAML documents
"""


import yaml


def build(settings, resources):
    """ Build RAML document for the resources
    """
    document_dict = _build_dict(settings, resources)
    document = '\n'.join([
        '#%RAML 1.0',
        '---',
        '{}'.format(yaml.dump(document_dict)),
        '...  # EOF',
    ])
    return document


def _build_dict(settings, resources):
    document_dict = {
        'title': settings['rapids.title'],
    }
    document_dict.update(_add(resources, None))
    return document_dict


def _add(resources, parent_class):
    tree = {}
    for resource in resources.get(parent_class, {}).values():
        uri_segment = '/{}'.format(resource['uri_segment'])
        tree[uri_segment] = _add(resources, resource['resource_class'])
    return tree


# EOF
