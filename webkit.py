"""
C'n'Safe Webkit Parser
======================

CSS transformer for Webkit.

"""

from . import _helpers

def transform(parser, keep_existant=True):
    string = ''

    for name, attributes in parser.items():
        string += parser.begin_section(name)
        for attribute, value in attributes.items():
            if keep_existant:
                string += parser.attribute(attribute, value)

            # Parsing attributes
            if attribute == 'border-radius':
                splitted_values = _helpers.split_values(value)
                positions = (
                    'top-left', 'top-right', 'bottom-right', 'bottom-left')
                for position, values in zip(positions, splitted_values):
                    string_values = ' / '.join(values)
                    string_position = '-webkit-border-%s-radius' % position
                    string += parser.attribute(string_position, string_values)
            elif 'border' in attribute and 'radius' in attribute:
                string += parser.attribute('-webkit-%s' % attribute, value)
            elif attribute == 'box-shadow':
                string += parser.attribute('-webkit-%s' % attribute, value)
            elif attribute.startswith('transition'):
                string += parser.attribute('-webkit-%s' % attribute, value)

        string += parser.end_section(name)

    return string
