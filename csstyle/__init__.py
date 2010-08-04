"""
CSStyle - CSS with Style
========================

CSStyle is a simple CSS parser generating CSS adapted for various browsers.

"""
import os
from copy import deepcopy

from . import gecko
from . import webkit
from . import presto
from ._helpers import odict

BROWSERS = ('gecko', 'webkit', 'presto')

class Parser(odict):
    """CSS parser."""
    def __init__(self, filenames=tuple(), text=''):
        """Parse ``filename``."""
        super(Parser, self).__init__()

        if isinstance(filenames, basestring):
            filenames = (filenames,)

        # TODO: @import are processed even when commented
        for filename in filenames:
            with open(filename) as fd:
                lines = fd.readlines()
                content = '\n'.join(lines)
                for line in lines:
                    if '@import' in line:
                        imported_file = \
                            line.strip(' ;\n').replace('@import', '').strip(' "\'')
                        content += open(os.path.join(os.path.dirname(filename), 
                                                     imported_file)).read()
                self._parse_sections(content)
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
                if isinstance(attributes, basestring):
                    string += attributes + '\n'
                elif isinstance(attributes, Parser):
                    string += repr(attributes) + '\n'
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
                            self[name].update(Parser(text=text))
                        else:
                            self[name] = Parser(text=text)
                        text = ''
                        in_multi_level = False
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