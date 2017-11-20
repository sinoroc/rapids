""" Decorators
"""


import venusian

from . import utility


def resource(*args, **kwargs):
    """ Class decorator
        The decorated class is added as a resource.
    """
    return _ResourceHelper(*args, **kwargs)


class _ResourceHelper:
    # pylint: disable=too-few-public-methods

    def __init__(self, uri_segment_pattern, parent_class):
        self._uri_segment_pattern = uri_segment_pattern
        self._parent_class = parent_class
        return

    def __call__(self, resource_class):
        venusian.attach(resource_class, self._callback)
        return resource_class

    def _callback(self, scanner, unused_name, resource_class):
        """ Callback for venusian
            Venusian is useful to have access to the Pyramid configuration
            from a decorator. This happens when the scan is performed.
        """
        util = scanner.config.registry.getUtility(utility.IUtility)
        util.add_resource(
            resource_class,
            self._uri_segment_pattern,
            self._parent_class,
        )
        return


def view(*args, **kwargs):
    """ Decorator allowing to add views
        This decorator works on functions and callable classes.
    """
    return _ViewHelper(*args, **kwargs)


class _ViewHelper:
    # pylint: disable=too-few-public-methods

    def __init__(self, resource_class):
        self._resource_class = resource_class
        return

    def __call__(self, view_callable):
        venusian.attach(view_callable, self._callback)
        return view_callable

    def _callback(self, scanner, unused_name, view_callable):
        util = scanner.config.registry.getUtility(utility.IUtility)
        util.add_view(view_callable, self._resource_class)
        return


# EOF
