""" REST APIs documented and sensible
"""


import pkginfo

from . import config
from . import decorators
from . import documents
from . import resources


# PEP 396
__version__ = pkginfo.Installed('rapids').version


# EOF
