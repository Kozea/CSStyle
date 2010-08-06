"""
CSStyle Presto Parser
=====================

CSS transformer for Presto-based browsers (Opera).

"""

from ._helpers import odict


def transform(parser, keep_existant=True):
    for name, attributes in parser.items():
        section = odict()

        if isinstance(attributes, str):
            parser[name] = odict()
            continue

        for attribute, value in attributes.items():
            if keep_existant:
                section[attribute] = value

            # Parsing attributes
            if attribute in ('text-overflow',):
                section['-o-%s' % attribute] = value
            elif attribute.startswith('transition'):
                section['-o-%s' % attribute] = value

        parser[name] = section

    return parser
