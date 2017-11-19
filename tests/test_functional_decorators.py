""" Functional test for decorators
"""


import unittest

import pyramid
import rapids
import webtest

import base


@rapids.decorators.resource('', None)
class Resource(rapids.resources.Base):
    """ Root resource
    """
    # pylint: disable=too-few-public-methods
    pass


def view(resource, unused_request):
    """ View for the root resource
    """
    return pyramid.httpexceptions.HTTPOk(resource.__name__)


class TestFunctional(base.Base, unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(settings=self.settings)
        self.config.include(rapids.config)
        self.config.add_view(view, context=Resource)
        self.config.scan('.')
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return

    def test_resources_decorator(self):
        """ GET on a decorated resource returns a successful response
        """
        self.test_application.get('/', status=200)
        return


# EOF
