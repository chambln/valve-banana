# keeb.py

import cfg


class Keeb:
    '''Provides methods for building a collection of complex key mappings'''

    def __init__(self, *maps):
        self.maps = list(maps)

    def __add__(self, other):
        return Keeb(*(self.maps + other.maps))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.pack())

    def __len__(self):
        return len(self.maps)
        
    def __bool__(self):
        return bool(self.maps)

    def __iter__(self):
        for map_ in self.maps:
            yield map_

    def __getitem__(self, key):
        return self.maps[key]

    def map(self, *args):
        '''Add a new complex key mapping'''
        self.maps.append(Map(*args))

    def pack(self):
        '''Organise this instance's maps into a dictionary'''
        pack = {}
        for m in self:
            mods = m.keycombo.modifiers
            final = m.keycombo.final
            if mods:
                # For now, this program can handle at most one modifier
                mod = mods[0]
            else:
                mod = 'none'
            if mod not in pack:
                pack[mod] = {}
            pack[mod][final] = m.action
        return pack

    def build(self):
        '''Return a list of cfg.Cfg() objects ready to write'''
        build = []
        for mod, binds in self.pack().items():
            c = cfg.Cfg(mod)
            for keyname, sentence in binds.items():
                c.bind(keyname, sentence)
                print('#', c)
            build += c
            print('Built', repr(c))
        return build
            

    def write(self, wd='./', dryrun=False):
        '''Write the files necessary to implement these mappings'''
        for part in self.build():
            part.path = wd + part.path
            if not dryrun:
                part.write()
            print('Wrote', part)


class Map:
    '''Represents a keycombo bound to an action'''

    def __init__(self, keystring, action):
        self.keycombo = Keycombo(keystring)
        self.action = action

    def __repr__(self):
        return "Map('{}', '{}')".format(self.keycombo, self.action)

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

print(k.build())
k.write(wd='./mybinds/', dryrun=True)
