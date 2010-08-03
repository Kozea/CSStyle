from copy import deepcopy

try:
    from itertools import izip, imap
except ImportError:
    imap = map
    map = lambda function, iterable: tuple(imap(function, iterable))
    izip = zip
    zip = lambda *iterables: tuple(izip(*iterables))


def split_values(values):
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


class odict(dict):
    def __init__(self):
        super(odict, self).__init__()
        self._keys = []

    def __delitem__(self, key):
        super(odict, self).__delitem__(key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        if key not in self:
            self._keys.append(key)
        super(odict, self).__setitem__(key, item)

    def update(self, dictionary):
        for key, value in dictionary.items():
            self[key] = value

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}
        d = memo.get(id(self))
        if d is not None:
            return d
        memo[id(self)] = d = self.__class__()
        dict.__init__(d, deepcopy(self.items(), memo))
        d._keys = self._keys[:]
        return d
        
    items = lambda self: zip(self._keys, self.values())

    iteritems = lambda self: izip(self._keys, self.itervalues())

    keys = lambda self: self._keys[:]

    iterkeys = lambda self: iter(self._keys)

    values = lambda self: map(self.get, self._keys)

    itervalues = lambda self: imap(self.get, self._keys)
 
    __iter__ = iterkeys

    __repr__ = lambda self: '{%s}' % ', '.join(
        '%s: %s' % (repr(key), repr(value)) for key, value in self.items())
