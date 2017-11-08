""" Functional test
"""


import unittest

import rapids


class TestFunctional(unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_functional(self):  # pylint: disable=no-self-use
        """ Functional test
        """
        hasattr(rapids, '__version__')
        return

# EOF
