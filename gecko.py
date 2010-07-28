"""
CSstyle Gecko Parser
====================

CSS transformer for Gecko-based browsers (Firefox).

"""

from ._helpers import odict


def transform(parser, keep_existant=True):
    for name, attributes in parser.items():
        section = odict()
        force_keep_existant = False

        # Parsing sections
        if '::selection' in name:
            parser[name] = {}
            name = name.replace('::selection', '::-moz-selection')
            force_keep_existant = True

        for attribute, value in attributes.items():
            if keep_existant or force_keep_existant:
                section[attribute] = value

            # Parsing attributes
            if attribute in ('border-radius', 'box-shadow'):
                section['-moz-%s' % attribute] = value
            elif 'border' in attribute and 'radius' in attribute:
                section['-moz-%s' % attribute] = value
            elif attribute.startswith('transition'):
                section['-moz-%s' % attribute] = value

        parser[name] = section

    return parser
