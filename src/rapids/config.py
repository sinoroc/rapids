""" Configuration
"""


import pyramid

from . import utility


def _add_resource(config, *args, **kwargs):
    util = config.registry.getUtility(utility.IUtility)
    return util.add_resource(*args, **kwargs)


def _build_documents(event):
    util = event.app.registry.getUtility(utility.IUtility)
    return util.build_documents()


def _root_factory(request, *args, **kwargs):
    util = request.registry.getUtility(utility.IUtility)
    return util.root_factory(request, *args, **kwargs)


def includeme(config):
    """ Include the library in the Pyramid application
    """
    util = utility.Utility(config.registry.settings)
    config.registry.registerUtility(util, utility.IUtility)
    config.add_directive('rapids_add_resource', _add_resource)
    config.add_subscriber(
        _build_documents,
        pyramid.events.ApplicationCreated,
    )
    config.set_root_factory(_root_factory)
    return


# EOF
