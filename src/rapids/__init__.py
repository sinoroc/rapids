""" REST APIs documented and sensible
"""


import pkg_resources

from . import config
from . import decorators
from . import documents
from . import resources


# PEP 396
__version__ = pkg_resources.get_distribution(
    'rapids',  # http://stackoverflow.com/a/22845276
).version


# EOF
