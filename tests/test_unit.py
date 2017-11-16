""" Functional test
"""


import unittest

import rapids
import pyramid.testing
import pyramid.view
import zope.interface


class TestProjectVersion(unittest.TestCase):
    """ Project version string
    """
    def test_project_has_version_string(self):
        """ Project should have a vesion string
        """
        try:
            rapids.__version__
        except AttributeError as version_exception:
            self.fail(version_exception)
        return


class TestAddResource(unittest.TestCase):
    """ Add resources
    """

    def setUp(self):
        self.config = pyramid.testing.setUp()
        self.config.include('rapids.config')
        return

    def tearDown(self):
        pyramid.testing.tearDown()
        return

    def test_add_valid_resource(self):
        """ Valid resources should be successfully added
        """
        class ValidResource(rapids.resources.Base):
            """ Valid resource
            """
            # pylint: disable=too-few-public-methods
            pass
        try:
            self.config.rapids_add_resource(ValidResource, '', None)
        except zope.interface.exceptions.DoesNotImplement as invalid_exception:
            self.fail(invalid_exception)
        return

    def test_add_invalid_resource(self):
        """ Invalid resources should not be added
        """
        class InvalidResource:
            """ Invalid resource
            """
            # pylint: disable=too-few-public-methods
            pass
        with self.assertRaises(zope.interface.exceptions.DoesNotImplement):
            self.config.rapids_add_resource(InvalidResource, '', None)
        return


# EOF
