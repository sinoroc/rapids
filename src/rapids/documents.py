""" Documents management
"""


from . import openapi
from . import raml


class Manager:
    """ Manager for documents
    """

    def __init__(self, config):
        self._config = config
        self._documents = {}
        return

    def build_documents(self, resources):
        """ Build documents for the resources
        """
        self._documents['application/openapi+yaml'] = openapi.build(
            self._config.registry.settings,
            resources,
        )
        self._documents['application/raml+yaml'] = raml.build(
            self._config.registry.settings,
            resources,
        )
        return

    def get_document(self, media_type):
        """ Get document for the media type
        """
        return self._documents[media_type]


# EOF
