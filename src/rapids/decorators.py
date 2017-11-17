""" Decorators
"""


import venusian

from . import utility


def resource(uri_segment, parent):
    """ Class decorator
    """
    return _ResourceHelper(uri_segment, parent)


class _ResourceHelper:
    # pylint: disable=too-few-public-methods

    def __init__(self, uri_segment, parent):
        self._uri_segment = uri_segment
        self._parent = parent
        return

    def __call__(self, decoratee):
        venusian.attach(decoratee, self._callback)
        return decoratee

    def _callback(self, scanner, unused_name, decoratee):
        """ Callback for venusian
            Venusian is useful to have access to the Pyramid configuration
            from a decorator. This happens when the scan is performed.
        """
        util = scanner.config.registry.getUtility(utility.IUtility)
        util.add_resource(
            decoratee,
            self._uri_segment,
            self._parent,
        )
        return


# EOF
