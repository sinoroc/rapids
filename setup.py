""" Setup script
"""


import os

import setuptools


NAME = 'rapids'
DESCRIPTION = "REST APIs documented and sensible"
URL = 'https://github.com/sinoroc/rapids'


AUTHOR = 'sinoroc'
AUTHOR_EMAIL = 'sinoroc.code+python@gmail.com'


REQUIREMENTS_INSTALL = [
    'pyramid',
    'PyYAML',
    'setuptools',  # needed for 'pkg_resources'
    'venusian',
    'zope.interface',
]

REQUIREMENTS_PACKAGE = [
    'wheel',
]

REQUIREMENTS_TEST = [
    'pytest',
    'pytest-pep8',
    'pytest-pylint',
    'readme_renderer',  # needed for 'python setup.py check --restructuredtext'
    'WebTest',
]

REQUIREMENTS_EXTRAS = {
    'develop': REQUIREMENTS_PACKAGE + REQUIREMENTS_TEST,
    'package': REQUIREMENTS_PACKAGE,
    'test': REQUIREMENTS_TEST,
}


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


CLASSIFIERS = [
    'Framework :: Pyramid',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


def _do_setup():
    setuptools.setup(
        name=NAME,
        version=VERSION,
        # metadata
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        classifiers=CLASSIFIERS,
        description=DESCRIPTION,
        license=LICENSE,
        long_description=LONG_DESCRIPTION,
        url=URL,
        # options
        extras_require=REQUIREMENTS_EXTRAS,
        install_requires=REQUIREMENTS_INSTALL,
        package_dir=PACKAGE_DIRECTORIES,
        packages=PACKAGES,
    )
    return


if __name__ == '__main__':
    _do_setup()


# EOF
