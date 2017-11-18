""" Decorators
"""


import venusian

from . import utility


def resource(uri_segment, parent_class):
    """ Class decorator
        The decorated class is added as a resource.
    """
    return _ResourceHelper(uri_segment, parent_class)


class _ResourceHelper:
    # pylint: disable=too-few-public-methods

    def __init__(self, uri_segment, parent_class):
        self._uri_segment = uri_segment
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
            self._uri_segment,
            self._parent_class,
        )
        return


# EOF
