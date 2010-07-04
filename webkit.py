"""
C'n'Safe Webkit Parser
======================

CSS transformer for Webkit.

"""

from . import _helpers

def transform(parser, keep_existant=True):
    for name, attributes in parser.items():
        section = {}

        for attribute, value in attributes.items():
            if keep_existant:
                section[attribute] = value

            # Parsing attributes
            if attribute == 'border-radius':
                splitted_values = _helpers.split_values(value)
                positions = (
                    'top-left', 'top-right', 'bottom-right', 'bottom-left')
                for position, values in zip(positions, splitted_values):
                    string_values = ' / '.join(values)
                    string_position = '-webkit-border-%s-radius' % position
                    section[string_position] = string_values
            elif 'border' in attribute and 'radius' in attribute:
                section['-webkit-%s' % attribute] = value
            elif attribute == 'box-shadow':
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('transition'):
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('transform'):
                section['-webkit-%s' % attribute] = value

        parser[name] = section

    return parser
