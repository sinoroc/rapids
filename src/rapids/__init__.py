""" Module initializer
"""


import pkg_resources


# PEP 396
__version__ = pkg_resources.get_distribution(
    'rapids',  # http://stackoverflow.com/a/22845276
).version


# EOF
