#!/usr/bin/env python


""" Setup script """


import os

import setuptools


NAME = 'rapids'
DESCRIPTION = "REST APIs documented and sensible"


AUTHOR = 'sinoroc'
AUTHOR_EMAIL = 'sinoroc.code+python@gmail.com'
URL = 'https://github.com/sinoroc/rapids'


LICENSE = 'Apache-2.0'  # https://spdx.org/licenses/


REQUIREMENTS_INSTALL = [
    'pyramid',
    'PyYAML',
    'setuptools',  # needed for 'pkg_resources'
    'venusian',
    'zope.interface',
]


REQUIREMENTS_PACKAGE = [
    'twine',
    'wheel',
]


REQUIREMENTS_TEST = [
    'pytest',
    'pytest-pep8',
    'pytest-pylint',
    'WebTest',
]


REQUIREMENTS_EXTRAS = {
    'package': REQUIREMENTS_PACKAGE,
    'test': REQUIREMENTS_TEST,
}


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
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst')) as file_:
        readme = file_.read()
    with open(os.path.join(here, 'CHANGELOG.rst')) as file_:
        changelog = file_.read()

    long_description = readme
    version = changelog.splitlines()[4]

    source_directory = 'src'
    packages = setuptools.find_packages(
        where=source_directory,
    )
    package_directories = {
        '': source_directory,
    }

    setuptools.setup(
        name=NAME,
        version=version,
        # metadata
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        classifiers=CLASSIFIERS,
        description=DESCRIPTION,
        license=LICENSE,
        long_description=long_description,
        url=URL,
        # options
        extras_require=REQUIREMENTS_EXTRAS,
        install_requires=REQUIREMENTS_INSTALL,
        package_dir=package_directories,
        packages=packages,
    )


if __name__ == '__main__':
    _do_setup()


# EOF
