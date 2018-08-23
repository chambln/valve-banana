# keymap.py

from cfg import Cfg

class Keymap:
    '''
    Collects key mappings and implements complex mappings using several 
    cfg files.
    '''

    def __init__(self, *maps):
        self.maps = list(maps)

    def append(self, map_):
        self.maps.append(map_)

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

    @property
    def master(self):
        '''Returns the subpack for which no modifiers are held'''
        return self.pack()['']  # Empty string represents no modifiers

    def build_group(self, modifier, subpack):
        '''
        Turns a modifier's part of the pack into a group of files that 
        implement it as a modifier keymap.

        Parameters:
            - modifier: single source engine keyname for the modifier 
              key.
            - subpack: dictionary keymap for which each key is a single 
              source engine keyname and the corresponding value is the 
              action it should produce.

        Returns (e.g. modifier='shift'):
            - Cfg('shift_dn')  -> Holds modified bindings
            - Cfg('shift_up')  -> Holds corresponding non-mod bindings
        '''
        # Initialise my UP and DOWN files for this group
        dn = Cfg(modifier+'_dn')
        up = Cfg(modifier+'_up')
        # I will need my master keymap for testing against later
        master = self.master
        for keyname, action in subpack.items():
            # Put this binding in my DOWN file
            dn.bind(keyname, action)
            if keyname in master:
                # If it exists, put the correspoding master binding into 
                # my UP file
                up.bind(keyname, master[keyname])
        # Print for debugging purposes
        print('Built', repr(master))
        return dn, up

    def build(self):
        '''
        Collect the built master and group keymaps to implement this 
        keymap.
        '''
        # We will build a list of instances of cfg.Cfg
        files = []
        # Pack myself up
        pack = self.pack()
        # First: Separate my master keymap (no modifiers) from the rest
        files.append(self.build_group())
        # Second: Build a group for each of my modifiers
        for modifier, subpack in pack.items():
            files.append(*self.build_group(modifier, subpack))
        # Finally, return the list of files
        print(files)
        return files

    def write(self):
        # build each build thingy iteratively shouldo nly take a ew lines


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
