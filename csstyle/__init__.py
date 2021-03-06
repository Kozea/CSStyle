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
CSStyle Parser
==============

Parser class for CSStyle.

"""

BROWSERS = ('webkit', 'presto', 'gecko', 'trident')
VERSION = "git"

import os

from . import gecko, webkit, presto, trident
from ._helpers import OrderedDict


class Parser(OrderedDict):
    """CSS parser."""
    def __init__(self, filenames=tuple(), text=''):
        """Parse ``filename``."""
        super(Parser, self).__init__()

        if isinstance(filenames, str):
            filenames = (filenames,)
        for filename in filenames:
            with open(filename) as file_descriptor:
                lines = [line.rstrip() + '\n'
                         for line in file_descriptor.readlines()]

            in_comment = False
            first_or_last_comment_line = False

            for line in lines:
                if '*/' in line:
                    in_comment = False
                    if line.split('*/')[-1] != '':
                        line = line.split('*/')[-1]
                        first_or_last_comment_line = True
                elif '/*' in line:
                    in_comment = True
                    if line.split('*/')[0] != '':
                        line = line.split('/*')[0]
                        first_or_last_comment_line = True
                if '@import' in line and (
                    first_or_last_comment_line or not in_comment):
                    first_or_last_comment_line = False
                    imported_file = \
                        line.strip(' ;\n').replace('@import', '').strip(' "\'')
                    if imported_file.startswith('url'):
                        imported_file = \
                            imported_file[3:].lstrip('("\'').rstrip('\'")')
                    text += open(os.path.join(
                            os.path.dirname(filename), imported_file)).read()
                else:
                    text += line
        self._parse_sections(text)

    def __nonzero__(self):
        return any(self.values())

    def __repr__(self):
        """Represent parsed CSS."""
        string = ''
        for name, attributes in self.items():
            if attributes:
                string += self.begin_section(name)
                if isinstance(attributes, str):
                    string += attributes
                elif isinstance(attributes, Parser):
                    string += repr(attributes)
                else:
                    for attribute, value in attributes.items():
                        string += self.attribute(attribute, value)
                string += self.end_section()

        return string

    @staticmethod
    def begin_section(name):
        """Return a section beginning string."""
        return '%s {\n' % name
        
    @staticmethod
    def end_section():
        """Return a section ending string."""
        return '}\n\n'
        
    @staticmethod
    def attribute(attribute, value):
        """Return an attribute string."""
        return '  %s: %s;\n' % (attribute, value)

    def _parse_sections(self, string):
        """Parse sections."""
        in_comment = False
        possible_comment_begin = False
        possible_comment_end = False
        text = ''
        brace_counter = 0

        # TODO: ignore /* and */ in strings
        for char in string:
            if in_comment:
                if char == '/' and possible_comment_end == True:
                    possible_comment_end = False
                    in_comment = False
                elif char == '*':
                    possible_comment_end = True
                else:
                    possible_comment_end = False
            else:
                if char == '{':
                    brace_counter += 1
                    if brace_counter == 1:
                        name = text.strip()
                        text = ''
                    else:
                        text += char
                elif char == '}':
                    brace_counter -= 1
                    if not brace_counter:
                        if self.get(name):
                            self[name].update(self._parse_attributes(text))
                        else:
                            self[name] = self._parse_attributes(text)
                        text = ''
                    else:
                        text += char
                        if self.get(name):
                            parser = Parser(text=text)
                            for key, value in parser.items():
                                if key in self[name]:
                                    self[name][key].update(value)
                                else:
                                    self[name][key] = value
                        else:
                            self[name] = Parser(text=text)
                        text = ''
                elif char == '*' and possible_comment_begin:
                    possible_comment_begin = False
                    in_comment = True
                    text = text[:-1]
                else:
                    possible_comment_begin = (char == '/')
                    text += char

    @staticmethod
    def _parse_attributes(string):
        """Parse and return attributes in section."""
        attributes = OrderedDict()

        if '{' in string:
            return string

        for expression in string.split(';'):
            expression = expression.strip()
            if expression:
                attribute, value = expression.split(':', 1)
                attributes[attribute.strip()] = value.strip()

        return attributes
