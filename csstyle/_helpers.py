"""
CSStyle various helpers for parsers

"""

from copy import deepcopy

# Python 2/3 support
# pylint: disable=W0622,C0103
try:
    from itertools import izip, imap
except ImportError:
    imap = map
    map = lambda function, iterable: tuple(imap(function, iterable))
    izip = zip
    zip = lambda *iterables: tuple(izip(*iterables))
# pylint: enable=W0622,C0103


def split_values(values):
    """Split given CSS attributes ``values``."""
    if '/' in values:
        values_list = [values_part.split() for values_part in values.split('/')]
    else:
        values_list = [values.split()]

    full_lists = []
    for values in values_list:
        if len(values) == 1:
            values = 4 * [values[0]]
        elif len(values) == 2:
            values = 2 * [values[0], values[1]]
        elif len(values) == 3:
            values = [values[0], values[1], values[2], values[1]]
        full_lists.append(values)

    return zip(*full_lists)

class OrderedDict(dict):
    """Dictionary that remembers insertion order."""
    # OrderedDict can access the _keys attribute of other dicts
    # pylint: disable=W0212
    def __init__(self):
        """Initialize an ordered dictionary."""
        super(OrderedDict, self).__init__()
        self._keys = []

    def __delitem__(self, key):
        """od.__delitem__(y) <==> del od[y]"""
        super(OrderedDict, self).__delitem__(key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        """od.__setitem__(i, y) <==> od[i]=y"""
        if key not in self:
            self._keys.append(key)
        super(OrderedDict, self).__setitem__(key, item)

    def update(self, dictionary):
        """D.update(E, **F) -> None.  Update D from dict/iterable E and F."""
        for key, value in dictionary.items():
            self[key] = value

    def __deepcopy__(self, memo=None):
        """Make a deep copy of od."""
        if memo is None:
            memo = {}
        dictionary = memo.get(id(self))
        if dictionary is not None:
            return dictionary
        memo[id(self)] = dictionary = self.__class__()
        dict.__init__(dictionary, deepcopy(self.items(), memo))
        dictionary._keys = self._keys[:]
        return dictionary
        
    items = lambda self: zip(self._keys, self.values())

    iteritems = lambda self: izip(self._keys, self.itervalues())

    keys = lambda self: self._keys[:]

    iterkeys = lambda self: iter(self._keys)

    values = lambda self: map(self.get, self._keys)

    itervalues = lambda self: imap(self.get, self._keys)
 
    __iter__ = iterkeys

    __repr__ = lambda self: '{%s}' % ', '.join(
        '%s: %s' % (repr(key), repr(value)) for key, value in self.items())

    # pylint: enable=W0212
