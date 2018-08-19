# keymap.py

import cfg

class Keymap:
    '''
    Collects key mappings and implements complex mappings using several 
    cfg files.
    '''

    def __init__(self, *maps):
        self.maps = list(maps)

    def append(self, element):
        self.maps.append(element)

    def map(self, *args):
        self.append(Map(*args))

    def __iter__(self):
        for map_ in self.maps:
            yield map_

    def __len__(self):
        return len(self.maps)

    def pack(self):
        pack = {}
        for map_ in self:
            # First, I get the relevant key names
            mods = map_.keycombo.modifiers
            final = map_.keycombo.final
            if mods:
                # For now, I can handle at most one modifier
                mod = mods[0]
            else:
                mod = ''
            # Make sure I support its modifier
            if mod not in pack:
                pack[mod] = {}
            # Add to my pack
            pack[mod][final] = map_.action
        return pack

    def build_master(self):
        pack = self.pack()
        master = cfg.Cfg('master')
        for keyname, action in pack.pop('').items():
            master.bind(keyname, action)
        print('Built', repr(master))
        return master

    def build(self):
        '''
        For each true modifier 'foo', create
          - Cfg('foo_dn')  -> Holds modified bindings
          - Cfg('foo_up')  -> Holds corresponding non-mod bindings
        ''' # TODO: make this docstring more formal

        # We will build a list of instances of cfg.Cfg
        files = []

        # Pack myself up
        pack = self.pack()

        # First: Separate my master (no modifiers) keymap from the rest
        files.append(self.build_master())
        
        # Second: Generate my modifier keymaps
        for mod, keymap in self.pack().items():
            pass

        # Finally, return the list of files
        print(files)
        return files


class Map:
    '''Represents any key combination bound to an action'''

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
k = Keymap()

k.map('enter', 'say')
k.map('shift-enter', 'say_team')
k.map('ctrl-enter', 'say glhf')
k.map('w', '+forward')
k.map('space', '+jump')

k.build()
