"""
C'n'Safe Presto Parser
======================

CSS transformer for Presto.

"""
from _helpers import odict

def transform(parser, keep_existant=True):
    for name, attributes in parser.items():
        section = odict()

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