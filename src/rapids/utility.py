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

    def __init__(self, config):
        self._documents_manager = documents.Manager(config)
        self._resources_manager = resources.Manager(config)
        return

    def add_resource(self, *args, **kwargs):
        """ Let the resources manager add a resource
        """
        return self._resources_manager.add_resource(*args, **kwargs)

    def add_view(self, *args, **kwargs):
        """ Let the resources manager add a view
        """
        return self._resources_manager.add_view(*args, **kwargs)

    def build_documents(self, *args, **kwargs):
        """ Let the documents manager build the documents
        """
        docs_manager = self._documents_manager
        resources_tree = self._resources_manager.resources_tree
        return docs_manager.build_documents(resources_tree, *args, **kwargs)

    def get_document(self, *args, **kwargs):
        """ Let the documents manager return a document
        """
        return self._documents_manager.get_document(*args, **kwargs)

    def get_root(self, *args, **kwargs):
        """ Let the resources manager return the Pyramid traversal root object
        """
        return self._resources_manager.get_root(*args, **kwargs)

    def view(self, *args, **kwargs):
        """ Let the resources manager build a response
        """
        return self._resources_manager.view(*args, **kwargs)


# EOF
