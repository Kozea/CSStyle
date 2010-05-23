"""
C'n'Safe - CSS Made Safe
========================

C'n'Safe is a simple CSS parser generating CSS adapted for various browsers.

"""

import gecko
import webkit

class Parser(dict):
    """CSS parser."""
    def __init__(self, filenames):
        """Parse ``filename``."""
        if isinstance(filenames, basestring):
            filenames = (filenames,)

        for filename in filenames:
            with open(filename) as fd:
                self._parse_sections(fd.read())

    def __repr__(self):
        """Represent parsed CSS."""
        string = ''

        for name, attributes in self.items():
            string += self.begin_section(name)
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
        string = string.replace('\n', '')

        in_comment = False
        possible_comment_begin = False
        possible_comment_end = False
        text = ''

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
                    name = text.strip()
                    text = ''
                elif char == '}':
                    if name in self:
                        self[name].update(self._parse_attributes(text))
                    else:
                        self[name] = self._parse_attributes(text)
                    text = ''
                elif char == '*' and possible_comment_start:
                    possible_comment_start = False
                    in_comment = True
                    text = text[:-1]
                else:
                    if char == '/':
                        possible_comment_start = True
                    text += char

    def _parse_attributes(self, string):
        """Parse and return attributes in section."""
        attributes = {}

        for expression in string.split(';'):
            expression = expression.strip()
            if expression:
                attribute, value = expression.split(':')
                attributes[attribute.strip()] = value.strip()

        return attributes
