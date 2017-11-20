""" Configuration
"""


import pyramid

from . import utility


def _add_resource(config, *args, **kwargs):
    util = config.registry.getUtility(utility.IUtility)
    return util.add_resource(*args, **kwargs)


def _add_view(config, *args, **kwargs):
    util = config.registry.getUtility(utility.IUtility)
    return util.add_view(*args, **kwargs)


def _build_documents(event):
    util = event.app.registry.getUtility(utility.IUtility)
    return util.build_documents()


def _get_root(request, *args, **kwargs):
    util = request.registry.getUtility(utility.IUtility)
    return util.get_root(request, *args, **kwargs)


def includeme(config):
    """ Include the library in the Pyramid application
    """
    util = utility.Utility(config)
    config.registry.registerUtility(util, utility.IUtility)
    config.add_directive('rapids_add_resource', _add_resource)
    config.add_directive('rapids_add_view', _add_view)
    config.add_subscriber(
        _build_documents,
        pyramid.events.ApplicationCreated,
    )
    config.set_root_factory(_get_root)
    return


# EOF
