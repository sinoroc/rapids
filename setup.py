""" Setup script
"""


import os

import setuptools


NAME = 'rapids'
DESCRIPTION = "rapids library"


INSTALL_REQUIREMENTS = [
]


HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGELOG.rst')) as f:
    CHANGELOG = f.read()


LONG_DESCRIPTION = README
VERSION = CHANGELOG.splitlines()[4]


SOURCE_DIRECTORY = 'src'
PACKAGES = setuptools.find_packages(
    where=SOURCE_DIRECTORY,
)
PACKAGE_DIRECTORIES = {
    '': SOURCE_DIRECTORY,
}


LICENSE = 'Apache-2.0'  # https://spdx.org/licenses/


def _do_setup():
    setuptools.setup(
        # metadata
        name=NAME,
        description=DESCRIPTION,
        license=LICENSE,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
        # options
        install_requires=INSTALL_REQUIREMENTS,
        package_dir=PACKAGE_DIRECTORIES,
        packages=PACKAGES,
    )
    return


if __name__ == '__main__':
    _do_setup()


# EOF
