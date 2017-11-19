""" Utility
"""


import zope.interface

from . import documents
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

    def __init__(self, settings):
        self._documents_manager = documents.Manager(settings)
        self._resources_manager = resources.Manager()
        return

    def add_resource(self, *args, **kwargs):
        """ Let the resources manager add a resource
        """
        return self._resources_manager.add_resource(*args, **kwargs)

    def build_documents(self, *args, **kwargs):
        """ Let the documents manager build the documents
        """
        docs_manager = self._documents_manager
        the_resources = self._resources_manager.resources
        return docs_manager.build_documents(the_resources, *args, **kwargs)

    def get_document(self, *args, **kwargs):
        """ Let the documents manager return a document
        """
        return self._documents_manager.get_document(*args, **kwargs)

    def get_root(self, *args, **kwargs):
        """ Let the resources manager return the Pyramid traversal root object
        """
        return self._resources_manager.get_root(*args, **kwargs)


# EOF
