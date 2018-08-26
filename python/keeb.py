# keeb.py

import low


class Keymap(object):
    '''Defines key combinations bound to actions'''

    def __init__(self, keymap={}):
        self.keymap = keymap

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.keymap)

    def __getitem__(self, key):
        if key not in self.keymap:
            # Fill out with dictionaries where needed
            self.keymap[key] = {}
        return self.keymap[key]

    def __setitem__(self, key, value):
        self.keymap[key] = value

    def __delitem__(self, key):
        del self.keymap[key]

    def __iter__(self):
        for group in self.keymap:
            yield group

    def map(self, *args):
        '''Implement a complex key mapping into my keymap dictionary'''
        m = Map(*args)
        # Get the relevant modifier (just one for now)
        mod = (*m.modifiers, 'none')[0]
        # Add this mapping to myself
        self[mod][m.final] = m.action

    def build(self):
        pass


class Map(object):
    '''Links a key combination to an action'''

    def __init__(self, keystring, action):
        self.keycombo = Keycombo(keystring)
        self.action = action

    def __len__(self):
        return len(self.modifiers) + 1

    @property
    def modifiers(self):
        return self.keycombo.modifiers

    @property
    def final(self):
        return self.keycombo.final


class Keycombo(object):
    '''Represents a combination of keys to be pressed simultaneously'''

    def __init__(self, keystring):
        self.keys = keystring.split('-')

    def __repr__(self):
        return "Keycombo('{}')".format('-'.join(self.keys))

    @property
    def modifiers(self):
        return self.keys[:-1]

    @property
    def final(self):
        return self.keys[-1]


def test_Keymap():
    k = Keymap()
    k.map('w', '+forward')
    k.map('enter', 'say')
    k.map('shift-enter', 'say_team')
    k.map('', 'exec sandbox')
    #k.map('ctrl-shift-enter', 'gg')
    print('repr(k) ==', repr(k))

def test_Map():
    m = Map('ctrl-k', 'kill')
    print('repr(m) ==', repr(m))

def test_Keycombo():
    kc = Keycombo('ctrl-shift-p')
    print('repr(kc) ==', repr(kc))
    print('repr(kc.modifiers) ==', repr(kc.modifiers))
    print('repr(kc.final) ==', repr(kc.final))

if __name__ == '__main__':
    test_Keymap()
