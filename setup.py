#!/usr/bin/env python

from distutils.core import setup

setup(name='unity-singlet',
    version='0.1',
    description='Simple Unity lens building library',
    author='Michael Hall',
    author_email='mhall119@ubuntu.com',
    license='GPLv3',
    url='http://launchpad.net/singlet',
    package_dir = {'': 'src'},
    packages=['singlet', 'singlet.lens', 'singlet.scope'],
)
