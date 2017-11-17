""" Configuration
"""


from . import utility


def _add_resource(config, *args, **kwargs):
    """ Add a resource
    """
    util = config.registry.getUtility(utility.IUtility)
    return util.add_resource(*args, **kwargs)


def _root_factory(request, *args, **kwargs):
    """ Root factory for Pyramid traversal
    """
    util = request.registry.getUtility(utility.IUtility)
    return util.root_factory(request, *args, **kwargs)


def includeme(config):
    """ Include the library in the Pyramid application
    """
    util = utility.Utility()
    config.registry.registerUtility(util, utility.IUtility)
    config.add_directive('rapids_add_resource', _add_resource)
    config.set_root_factory(_root_factory)
    return


# EOF
