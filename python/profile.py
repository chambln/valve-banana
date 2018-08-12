# profile.py
# vim: fdm=marker

import writer
import pprint


class Profile(object):
    '''Holds a collection of methods for building a user's config'''

    def __init__(self):
        self.keymap = Keymap()
        self.modes = []

    def map(self, *args):
        self.keymap.map(*args)


class Keymap(object):
    '''Describes all key mappings in one big data structure'''

    def __init__(self, *maps):
        self.maps = list(*maps)

    def __repr__(self):
        return pprint.pformat(self.build())

    def __str__(self):
        return '\n'.join((str(m) for m in self))

    def __add__(self, other):
        return Keymap(*(self.maps + other.maps))

    def __bool__(self):
        return bool(self.maps)

    def __iter__(self):
        for m in self.maps:
            yield m

    def __getitem__(self, key):
        return self.maps[key]

    def build(self):
        '''Build up the keymap structure from the individual Map() objects'''
        keymap = {}
        for m in self:
            # Just take first modifier (for now)
            mod = m.modifiers[-1]
            # Make sure the keymap supports this modifier
            if mod not in keymap:
                keymap[mod] = {}
            # Add this m to self.keymap
            keymap[mod][m.key] = m.action
        return keymap

    def map(self, *args):
        self.append(Map(*args))

    def append(self, mapping):
        self.maps.append(mapping)


class Map(object):
    '''Describes how a key combination should map to an action'''

    def __init__(self, keystring, action):
        self.keycombo = Keycombo(keystring)
        self.action = action

    def __str__(self):
        return 'Map {} -> {}'.format(self.keycombo, self.action)

    def __bool__(self):
        return bool(self.action)

    @property
    def key(self):
        return self.keycombo.key

    @property
    def modifiers(self):
        return self.keycombo.modifiers
    
    
class Keycombo(object):
    '''Describes a key or combination of keys'''

    def __init__(self, keystring):
        self.keys = keystring.split('-')

    def __str__(self):
        return '-'.join(self.keys)

    @property
    def key(self):
        return self.keys[-1]

    @property
    def modifiers(self):
        if len(self.keys) > 1:
            return self.keys[:-1]
        else:
            return ['none']


p = Profile()
p.map('a', '+moveleft')
p.map('s', '+back')
p.map('d', '+moveright')
p.map('space', '+jump')
p.map('enter', 'say')
p.map('shift-enter', 'say_team')
p.map('ctrl-k', 'kill')
p.map('ctrl-shift-s', 'exec sandbox.cfg')
print(repr(p))
