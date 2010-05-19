"""
C'n'Safe - CSS Made Safe
========================

TODO: write documentation

"""

class Parser(dict):
    """TODO: docstring."""
    def __init__(self, filenames):
        """TODO: docstring."""
        if isinstance(filenames, basestring):
            filenames = (filenames,)

        for filename in filenames:
            with open(filename) as fd:
                self._parse_blocks(fd.read())

    def __repr__(self):
        """TODO: docstring."""
        string = ''

        for name, attributes in self.items():
            string += '%s {\n' % name
            for attribute, value in attributes.items():
                string += '  %s: %s;\n' % (attribute, value)
            string += '}\n\n'

        return string

    def _parse_blocks(self, string):
        """TODO: docstring."""
        blocks = {}
        string = string.replace('\n', '')

        in_block = False
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
                    in_block == True
                    name = text.strip()
                    text = ''
                elif char == '}':
                    in_block == False
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
        """TODO: docstring."""
        attributes = {}

        for expression in string.split(';'):
            expression = expression.strip()
            if expression:
                attribute, value = expression.split(':')
                attributes[attribute.strip()] = value.strip()

        return attributes
