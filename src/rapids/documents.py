""" Documents management
"""


from . import raml


class Manager:
    """ Manager for documents
    """

    def __init__(self, settings):
        self._settings = settings
        self._documents = {}
        return

    def build_documents(self, resources):
        """ Build documents for the resources
        """
        self._documents['application/raml+yaml'] = raml.build(
            self._settings,
            resources,
        )
        return

    def get_document(self, media_type):
        """ Get document for the media type
        """
        return self._documents[media_type]


# EOF
