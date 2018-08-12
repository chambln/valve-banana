# keymap.py
# vim: fdm=marker

class Keymap(Spec):
    '''Holds a dictionary of values that represent both modified and unmodified 
    key mappings'''

    def __init__(self, mappings, ):
        self.maps = maps  # List of Map() objects

    def build(self):
        '''Build the keymap dictionary to be built from ... then something else 
        before returning maybe? Honestly idk at this point my brain feels like 
        jelly'''
        pass


class Map(object):
    '''Specifies how a key combination should map to an action'''

    def __init__(self, keycombo, action):
        self.keycombo = keycombo  # Keycombo() object
        self.action = action      # Action() object

    def __str__(self):
        return 'map {} "{}"'.format(self.keycombo, self.action)

    def build(self):
        print("Building:", self)
        if self.keycombo.modifier:
            # Modified map builder
            pass
        else:
            # Build with no modifiers
            # Return something that the Profile().Keymap() can use to build its 
            # keymap dictionary from
            pass


class Keycombo(object):
    # docstring {{{
    '''\
    Represents an arbitrary key or combination thereof; i.e (<modifier>-)*key.

    Examples:
        'enter'   ->  Keycombo('enter')
        'alt-p'   ->  Keycombo('alt', 'p')
        'ctrl-r'  ->  Keycombo('ctrl', 'r')
    ''' # }}}

    def __init__(self, *keys):
        self.modificand = self.keys[-1]
        self.modifier = self.keys[:-1]

    def __str__(self):
        return '-'.join(self.keys)
