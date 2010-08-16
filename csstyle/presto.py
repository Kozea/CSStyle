"""
CSStyle Presto Parser
=====================

CSS transformer for Presto-based browsers (Opera).

"""

from ._helpers import OrderedDict


def transform(parser, keep_existant=True):
    """Add Presto-specific attributes to ``parser``."""
    for name, attributes in parser.items():
        section = OrderedDict()

        if isinstance(attributes, str):
            parser[name] = OrderedDict()
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
