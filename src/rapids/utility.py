""" Utility
"""


import zope.interface

from . import resources


class IUtility(zope.interface.Interface):
    """ Interface for the utility
    """
    # pylint: disable=inherit-non-class
    pass


@zope.interface.implementer(IUtility)
class Utility:
    """ Utility
        Belongs in Pyramid's config registry.
        Thin interface that simply redirects the calls to the specialzed
        utility objects.
    """

    def __init__(self):
        self._resources_manager = resources.Manager()
        return

    def add_resource(self, *args, **kwargs):
        """ Add resource
        """
        return self._resources_manager.add_resource(*args, **kwargs)

    def root_factory(self, *args, **kwargs):
        """ Root factory for Pyramid traversal
        """
        return self._resources_manager.root_factory(*args, **kwargs)


# EOF
