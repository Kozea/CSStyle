"""
C'n'Safe Gecko Parser
=====================

CSS transformer for Gecko.

"""

def transform(parser, keep_existant=True):
    for name, attributes in parser.items():
        section = {}

        for attribute, value in attributes.items():
            if keep_existant:
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
