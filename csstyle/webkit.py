"""
CSStyle Webkit Parser
=====================

CSS transformer for Webkit-based browsers (Safari, Chrome).

"""

from ._helpers import OrderedDict, split_values


def transform(parser, keep_existant=True):
    """Add Webkit-specific attributes to ``parser``."""
    for name, attributes in parser.items():
        section = OrderedDict()
        force_keep_existant = False

        # Parsing sections
        if '@keyframes' in name:
            parser[name] = {}
            new_name = name.replace('@keyframes', '@-webkit-keyframes')
            parser[new_name] = transform(attributes, keep_existant)
            continue
        if '::placeholder' in name:
            parser[name] = {}
            name = name.replace('::placeholder', '::-webkit-input-placeholder')
            force_keep_existant = True

        if isinstance(attributes, str):
            parser[name] = OrderedDict()
            continue

        for attribute, value in attributes.items():
            if keep_existant or force_keep_existant:
                section[attribute] = value

            # Parsing attributes
            if attribute == 'border-radius':
                splitted_values = split_values(value)
                positions = (
                    'top-left', 'top-right', 'bottom-right', 'bottom-left')
                for position, values in zip(positions, splitted_values):
                    string_values = ' / '.join(values)
                    string_position = '-webkit-border-%s-radius' % position
                    section[string_position] = string_values
            elif attribute == 'text-outline' or attribute == 'text-stroke':
                section['-webkit-text-stroke'] = value
            elif attribute == 'box-reflect':
                for inner_attribute in ('gradient',):
                    value = value.replace(' %s' % inner_attribute,
                                          ' -webkit-%s' % inner_attribute)
                section['-webkit-%s' % attribute] = value
            elif 'border' in attribute and 'radius' in attribute:
                section['-webkit-%s' % attribute] = value
            elif attribute == 'appearance':
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('animation'):
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('transition'):
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('transform'):
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('column'):
                section['-webkit-%s' % attribute] = value
            elif attribute.startswith('box'):
                section['-webkit-%s' % attribute] = value

            for gradient_type in (
                'linear', 'radial', 'repeating-linear', 'repeating-radial'):
                full_type = '%s-gradient' % gradient_type
                if hasattr(value, 'startswith') and value.startswith(full_type):
                    section[attribute] = value.replace(
                        full_type, '-webkit-%s' % full_type)

        parser[name] = section

    return parser
