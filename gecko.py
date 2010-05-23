"""
C'n'Safe Webkit Parser
======================

CSS transformer for Gecko.

"""

def transform(parser, keep_existant=True):
    string = ''

    for name, attributes in parser.items():
        string += parser.begin_section(name)
        for attribute, value in attributes.items():
            if keep_existant:
                string += parser.attribute(attribute, value)

            # Parsing attributes
            if attribute in ('border-radius', 'box-shadow'):
                string += parser.attribute('-moz-%s' % attribute, value)
            elif 'border' in attribute and 'radius' in attribute:
                string += parser.attribute('-moz-%s' % attribute, value)
            elif attribute.startswith('transition'):
                string += parser.attribute('-moz-%s' % attribute, value)

        string += parser.end_section(name)

    return string
