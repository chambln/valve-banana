# keeb.py


class Keeb:
    '''Provides methods for building a collection of complex key mappings'''

    def __init__(self, maps=[]):
        self.maps = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.build())

    def map(self, *args):
        self.maps.append(Map(*args))

    def build(self):
        keeb = {}
        for m in self.maps:
            mods = m.keycombo.modifiers
            final = m.keycombo.final
            if mods:
                # For now, this program can handle at most one modifier
                mod = mods[0]
            else:
                mod = 'none'
            if mod not in keeb:
                keeb[mod] = {}
            keeb[mod][final] = m.action
        return keeb


class Map:
    '''Represents a keycombo bound to an action'''

    def __init__(self, keystring, action):
        self.keycombo = Keycombo(keystring)
        self.action = action

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} -> {}'.format(self.keycombo, self.action)


class Keycombo:
    '''Describes a key press or combination thereof'''

    def __init__(self, keystring):
        self.keys = keystring.split('-')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '-'.join(self.keys)

    @property
    def modifiers(self):
        return self.keys[:-1]

    @property
    def final(self):
        return self.keys[-1]


# TESTING
k = Keeb()

k.map('enter', 'say')
k.map('shift-enter', 'say_team')
k.map('w', '+forward')
k.map('s', '+back')
k.map('a', '+moveleft')
k.map('d', '+moveright')
k.map('space', '+jump')

print(k)
