""" Configuration
"""


from . import resources


def _add_resource(config, resource, uri_segment, parent):
    """ Add a resource
    """
    manager = config.registry.getUtility(resources.IManager)
    return manager.add_resource(resource, uri_segment, parent)


def includeme(config):
    """ Include the library in the Pyramid application
    """
    manager = resources.Manager()
    config.registry.registerUtility(manager, resources.IManager)
    config.add_directive('add_resource', _add_resource)
    config.set_root_factory(resources.root_factory)
    return


# EOF
