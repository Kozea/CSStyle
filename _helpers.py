from itertools import izip, imap
from copy import deepcopy
        
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

# -*- coding: utf-8 -*-

class odict(dict):
    def __init__(self):
        dict.__init__(self)
        self._keys = []

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        if key not in self:
            self._keys.append(key)
        dict.__setitem__(self, key, item)

    def items(self):
        return zip(self._keys, self.values())

    def iteritems(self):
        return izip(self._keys, self.itervalues())

    def keys(self):
        return self._keys[:]

    def iterkeys(self):
        return iter(self._keys)

    def values(self):
        return map(self.get, self._keys)

    def itervalues(self):
        return imap(self.get, self._keys)
 
    __iter__ = iterkeys

#dic = {}
#dic['1'] = 10
#dic['5'] = 6
#dic['2'] = 3

#for key in dic.keys():
    #print '%s : %s' % (key, dic[key])