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

import os
from copy import deepcopy

from . import gecko
from . import webkit
from . import presto
from ._helpers import odict

VERSION = "0.1"

BROWSERS = ('webkit', 'presto', 'gecko')

class Parser(odict):
    """CSS parser."""
    def __init__(self, filenames=tuple(), text=''):
        """Parse ``filename``."""
        super(Parser, self).__init__()

        if isinstance(filenames, str):
            filenames = (filenames,)
        for filename in filenames:
            with open(filename) as fd:
                lines = [line.strip() for line in fd.readlines()]
                text += ''.join(lines)
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
                    if '@import' in line and (first_or_last_comment_line or not in_comment):
                        first_or_last_comment_line = False
                        imported_file = \
                            line.strip(' ;\n').replace('@import', '').strip(' "\'')
                        text += open(os.path.join(os.path.dirname(filename), 
                                                     imported_file)).read()
        self._parse_sections(text)
    
    def __nonzero__(self):
        for name, attributes in self.items():
            if attributes:
                return True
        return False
                
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
                string += self.end_section(name)

        return string

    def begin_section(self, name):
        """Return a section beginning string."""
        return '%s {\n' % name
        
    def end_section(self, name):
        """Return a section ending string."""
        return '}\n\n'
        
    def attribute(self, attribute, value):
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
                        in_multi_level = True
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
                                    self[name][key].update(parser[key])
                                else:
                                    self[name][key] = parser[key]
                        else:
                            self[name] = Parser(text=text)
                        text = ''
                elif char == '*' and possible_comment_start:
                    possible_comment_start = False
                    in_comment = True
                    text = text[:-1]
                else:
                    possible_comment_start = (char == '/')
                    text += char

    def _parse_attributes(self, string):
        """Parse and return attributes in section."""
        attributes = odict()

        if '{' in string:
            return string

        for expression in string.split(';'):
            expression = expression.strip()
            if expression:
                attribute, value = expression.split(':', 1)
                attributes[attribute.strip()] = value.strip()

        return attributes
