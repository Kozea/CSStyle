"""
CSStyle Trident Parser
======================

CSS transformer for Microsoft Internet Explorer

"""

from ._helpers import OrderedDict


def transform(parser, keep_existant=True):
    """Add Trident-specific attributes to ``parser``."""
    for name, attributes in parser.items():
        section = OrderedDict()

        for attribute, value in attributes.items():
            if keep_existant:
                section[attribute] = value

            if attribute.startswith('transform'):
                section['-ms-%s' % attribute] = value

            for gradient_type in (
                'linear', 'radial', 'repeating-linear', 'repeating-radial'):
                full_type = '%s-gradient' % gradient_type
                if hasattr(value, 'startswith') and \
                        value.startswith(full_type):
                    section[attribute] = value.replace(
                        full_type, '-ms-%s' % full_type)

        parser[name] = section

    return parser
