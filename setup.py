#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of CSStyle
# Copyright © 2010 Kozea
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CSStyle.  If not, see <http://www.gnu.org/licenses/>.

"""
CSStyle - CSS with Style
========================

CSStyle is a simple CSS parser generating CSS adapted for various browsers.

CSStyle Project runs on most of the UNIX-like platforms (Linux, BSD,
MacOS X) and Windows.It is free and open-source software, released under GPL
version 3.

For further information, please visit the `Radicale Website
<http://www.radicale.org/>`_.

"""

import os
from distutils.core import setup
from distutils.command.build_scripts import build_scripts

import csstyle


# build_scripts is known to have a lot of public methods
# pylint: disable=R0904
class BuildScripts(build_scripts):
    """Build the package."""
    def run(self):
        """Run building."""
        # These lines remove the .py extension from the radicale executable
        self.mkpath(self.build_dir)
        for script in self.scripts:
            root, _ = os.path.splitext(script)
            self.copy_file(script, os.path.join(self.build_dir, root))
# pylint: enable=R0904


# When the version is updated, ``csstyle.VERSION`` must be modified.
# A new section in the ``NEWS`` file must be added too.
setup(
    name="CSStyle",
    version=csstyle.VERSION,
    description="CSStyle is a simple CSS parser generating CSS adapted for" + \
                " various browsers.",
    long_description=__doc__,
    author="Kozea",
    author_email="guillaume.ayoub@kozea.fr",
    url="http://www.csstyle.org/",
    download_url="http://gitorious.org/csstyle/csstyle/archive-tarball/master",
    license="GNU GPL v3",
    platforms="Any",
    packages=["csstyle"],
    provides=["csstyle"],
    scripts=["csstyle.py"],
    cmdclass={"build_scripts": BuildScripts},
    keywords=["css", "generator"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Topic :: Software Development :: Code Generators"])
