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


def _get_root(request, *args, **kwargs):
    util = request.registry.getUtility(utility.IUtility)
    return util.get_root(request, *args, **kwargs)


class _ViewDeriver:
    # pylint: disable=too-few-public-methods

    options = (
        'rapids',
    )

    def __init__(self, view, info):
        self._view = view
        self._util = None
        if info.options.get('rapids', None) is not None:
            self._util = info.registry.getUtility(utility.IUtility)
            self._util.add_view(**info.options)
        return

    def __call__(self, *args, **kwargs):
        response = None
        if self._util is not None:
            response = self._util.view(self._view, *args, **kwargs)
        else:
            response = self._view(*args, **kwargs)
        return response


def includeme(config):
    """ Include the library in the Pyramid application
    """
    util = utility.Utility(config)
    config.registry.registerUtility(util, utility.IUtility)
    config.add_directive('rapids_add_resource', _add_resource)
    config.add_view_deriver(_ViewDeriver)
    config.add_subscriber(
        _build_documents,
        pyramid.events.ApplicationCreated,
    )
    config.set_root_factory(_get_root)
    return


# EOF
